import SimpleITK
import numpy as np

from pandas import DataFrame
from scipy.ndimage import center_of_mass, label
import torchvision
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor
import torch
from evalutils import DetectionAlgorithm
from evalutils.validators import (
    UniquePathIndicesValidator,
    UniqueImagesValidator,
)
from skimage import transform
import json

class Noduledetection(DetectionAlgorithm):
    def __init__(self):
        super().__init__(
            validators=dict(
                input_image=(
                    UniqueImagesValidator(),
                    UniquePathIndicesValidator(),
                )
            ),
        )
        
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print("==> Using ", self.device)
        print("==> Initializing model")
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False)
        num_classes = 2  # 1 class (nodule) + background
        in_features = self.model.roi_heads.box_predictor.cls_score.in_features
        self.model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
        self.model.load_state_dict(
            torch.load(
                "model",
                map_location=self.device,
            )
        ) 
        self.model.to(self.device)
        self.model.eval()  # set to inference mode
        print("==> Weights loaded")
        
    def predict(self, *, input_image: SimpleITK.Image) -> DataFrame:
        '''
        {
            "type": "Multiple 2D bounding boxes",
            "boxes": [
                {
                "corners": [
                    [ 92.66666412353516, 136.06668090820312, 0.5009999871253967],
                    [ 54.79999923706055, 136.06668090820312, 0.5009999871253967],
                    [ 54.79999923706055, 95.53333282470703, 0.5009999871253967],
                    [ 92.66666412353516, 95.53333282470703, 0.5009999871253967]
                ]},
                {
                "corners": [
                    [ 92.66666412353516, 136.06668090820312, 0.5009999871253967],
                    [ 54.79999923706055, 136.06668090820312, 0.5009999871253967],
                    [ 54.79999923706055, 95.53333282470703, 0.5009999871253967],
                    [ 92.66666412353516, 95.53333282470703, 0.5009999871253967]
                ]}
            ],
            "version": { "major": 1, "minor": 0 }
        }
        '''
        print('predict function is called')
        
        image_data = SimpleITK.GetArrayFromImage(input_image)
        spacing = input_image.GetSpacing()
        image_data = np.array(image_data)
        shape = image_data.shape
        print(image_data.shape)

        # Pre-process the image
        image = transform.resize(image_data, (1024, 1024))  # resize all images to 512 x 512 in shape
        #the range should be from 0 to 1.
        image = image.astype(np.float32) / np.max(image)  # normalize
        image = np.expand_dims(image, axis=0)
        tensor_image = torch.from_numpy(image).to(self.device).reshape(1, 1024, 1024)
        print(self.device)
        with torch.no_grad():
            prediction = self.model([tensor_image.to(self.device)])
            
        print('prediction ', prediction)
        data = {}
        data['type']="Multiple 2D bounding boxes"
        data['boxes'] = []
        for element in range(len(prediction[0]["boxes"])):
            box = {}   
            box['corners']=[]
            boxes = prediction[0]["boxes"][element].cpu().numpy()
            score = np.round(prediction[0]["scores"][element].cpu().numpy(),
                            decimals= 4)
            x_min, x_max, y_min, y_max = boxes[0]*spacing[0], boxes[2]*spacing[0], boxes[1]*spacing[1],  boxes[3]*spacing[1]
            bottom_left = [x_min, y_min,  0.5009999871253967] 
            bottom_right = [x_max, y_min,  0.5009999871253967]
            top_left = [x_min, y_max,  0.5009999871253967]
            top_right = [x_max, y_max,  0.5009999871253967]
            box['corners'].extend([top_right, top_left, bottom_left, bottom_right])
            data['boxes'].append(box)
        
        data['version'] = { "major": 1, "minor": 0}
        # Convert serialized candidates to a pandas.DataFrame
        print('data here', data)
        with open('/output/nodules.json', "w") as f:
            json.dump(data, f)

        # Convert serialized candidates to a pandas.DataFrame
        return DataFrame(data)

if __name__ == "__main__":
    Noduledetection().process()
