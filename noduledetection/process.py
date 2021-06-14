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
from typing import Dict
import training_utils.utils as utils
from training_utils.dataset import CXRNoduleDataset, get_transform
import os
from training_utils.train import train_one_epoch

class Noduledetection(DetectionAlgorithm):
    def __init__(self, train=False):
        super().__init__(
            validators=dict(
                input_image=(
                    UniqueImagesValidator(),
                    UniquePathIndicesValidator(),
                )
            ),
            output_file = '/output/nodules.json'
        )
        
        #------------------------------- LOAD the model here ---------------------------------
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = torchvision.models.detection.fasterrcnn_resnet50_fpn(pretrained=False, pretrained_backbone=False)
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
            
        
    def process(self):
        self.load()
        self.validate()
        self.process_cases()
        self.save()

    def process_cases(self, file_loader_key: str = None):
        if file_loader_key is None:
            file_loader_key = self._index_key
        self._case_results = []
        for idx, case in self._cases[file_loader_key].iterrows():
            self.process_case(idx=idx, case=case)
        
    def process_case(self, *, idx, case):
        # Load and test the image for this case
        input_image, input_image_file_path = self._load_input_image(case=case)
        # Detect and score candidates
        scored_candidates = self.predict(input_image=input_image)
        self._case_results = scored_candidates
        
        
    def retrain(self, input_dir, output_dir, num_epochs = 2):
        # create training dataset and defined transformations
        self.model.train() 
        dataset = CXRNoduleDataset(input_dir, os.path.join(input_dir, 'metadata.csv'), get_transform(train=True))

        # define training and validation data loaders
        data_loader = torch.utils.data.DataLoader(
            dataset, batch_size=2, shuffle=True, num_workers=4,
            collate_fn=utils.collate_fn)
    
        # construct an optimizer
        params = [p for p in self.model.parameters() if p.requires_grad]
        optimizer = torch.optim.SGD(params, lr=0.005,
                                    momentum=0.9, weight_decay=0.0005)
        # and a learning rate scheduler
        lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                       step_size=3,
                                                       gamma=0.1)        
        for epoch in range(num_epochs):
            train_one_epoch(self.model, optimizer, data_loader, self.device, epoch, print_freq=10)
            # update the learning rate
            lr_scheduler.step()
            # evaluate on the test dataset
            
        # save retrained version  
        torch.save(self.model.state_dict(), os.path.join(output_dir, "model_v2"))
      

    def format_to_GC(self, np_prediction, spacing, z_coord = 0.5) -> Dict:
        '''
        np_prediction: dictionary with keys boxes and scores.
        np_prediction[boxes] holds coordinates in the format as x1,y1,x2,y2
        spacing :  pixel spacing for x and y coordinates.
        
        return:
        a Dict in line with grand-challenge.org format.
        '''
        data = {}
        data['type']="Multiple 2D bounding boxes"
        data['boxes'] = []
        for i, bb in enumerate(np_prediction['boxes']):
            box = {}   
            box['corners']=[]
            x_y_spacing = [spacing[0], spacing[1], spacing[0], spacing[1]]
            x_min, y_min, x_max, y_max = bb*x_y_spacing
            bottom_left = [x_min, y_min,  z_coord] 
            bottom_right = [x_max, y_min,  z_coord]
            top_left = [x_min, y_max,  z_coord]
            top_right = [x_max, y_max,  z_coord]
            box['corners'].extend([top_right, top_left, bottom_left, bottom_right])
            box['probability'] = float(np_prediction['scores'][i])
            data['boxes'].append(box)
        data['version'] = { "major": 1, "minor": 0}
        
        return data
        
    def predict(self, *, input_image: SimpleITK.Image) -> DataFrame:
        self.model.eval() 
        
        image_data = SimpleITK.GetArrayFromImage(input_image)
        spacing = input_image.GetSpacing()
        image_data = np.array(image_data)
        shape = image_data.shape

        # Pre-process the image
        image = transform.resize(image_data, (1024, 1024))  # resize all images to 1024 x 1024 in shape
        #the range should be from 0 to 1.
        image = image.astype(np.float32) / np.max(image)  # normalize
        image = np.expand_dims(image, axis=0)
        tensor_image = torch.from_numpy(image).to(self.device).reshape(1, 1024, 1024)
        with torch.no_grad():
            prediction = self.model([tensor_image.to(self.device)])
            
        # convert predictions from tensor to numpy array.
        np_prediction = {str(key):[i.cpu().numpy() for i in val]
               for key, val in prediction[0].items()}
        data = self.format_to_GC(np_prediction, spacing)
        return data

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(
        prog='process.py',
        description=
            'Reads all images from an input directory and produces '
            'results in an output directory')

    parser.add_argument('input_dir', help = "input directory to process")
    parser.add_argument('output_dir', help = "output directory generate result files in")
    parser.add_argument('--train', action='store_true', help = "Algorithm on train mode.")

    parsed_args = parser.parse_args()    
    if parsed_args.train:
        Noduledetection(parsed_args.train).retrain(parsed_args.input_dir, parsed_args.output_dir)
    else:
        Noduledetection().process()
            
    
   
    
    
    
    
    
