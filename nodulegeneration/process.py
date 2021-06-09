import SimpleITK
import numpy as np

from evalutils import SegmentationAlgorithm
from evalutils.validators import (
    UniquePathIndicesValidator,
    UniqueImagesValidator,
)
from utils import *
from typing import Dict
import json
from skimage.measure import regionprops


class Nodulegeneration(SegmentationAlgorithm):
    def __init__(self):
        super().__init__(
            validators=dict(
                input_image=(
                    UniqueImagesValidator(),
                    UniquePathIndicesValidator(),
                )
            ),
        )
        
        # load nodules.json for location
        with open("/input/nodules.json") as f:
            self.data = json.load(f)
    

    def get_nodule_diameter(self, seg_image):
        
        seg_image = np.mean(seg_image, axis=1)
        seg_image[seg_image!=0] = 255
        seg_image = seg_image.astype(int)
        properties = regionprops(seg_image)

        for p in properties:
            min_row, min_col, max_row, max_col = p.bbox
            diameter = max(max_row - min_row, max_col - min_col)
            print(diameter)

        return diameter
    

    def process_CT_patches(self, ct_path, seg_path, required_diameter):
        '''
        Resample ct nodule patches and generates fake CXR nodule patches.
        '''
        ct_image = SimpleITK.GetArrayFromImage(SimpleITK.ReadImage(ct_path))
        seg_img = SimpleITK.GetArrayFromImage(SimpleITK.ReadImage(seg_path))
        diameter = self.get_nodule_diameter(seg_img)
        scaling_factor = diameter/required_diameter

        image_resampled, new_spacing = resample(ct_image, voxel_spacing = [1,1,1], new_spacing=[scaling_factor,scaling_factor,scaling_factor])
        seg_image_resampled, new_spacing = resample(seg_img, voxel_spacing = [1,1,1], new_spacing=[scaling_factor,scaling_factor,scaling_factor])
        # put black values to the ct patch outside nodules.
        image_resampled[seg_image_resampled<=np.min(seg_image_resampled)]=np.min(image_resampled)
        # generate 2D digitially reconstructed CXR.
        X_ct_2d_resampled = generate_2d(image_resampled)
        
        return X_ct_2d_resampled


    def predict(self, *, input_image: SimpleITK.Image) -> SimpleITK.Image:
        # TODO
        '''
        1. Concat images as 3d by keeping the spacing info
        2. Handle when ct patch size is different than bb.
        3. Get good coordinates by looking at the lung segmentations for each image.
        4. Handle multiple nodules per slice
        '''
        # for memory issues
        input_image = SimpleITK.GetArrayFromImage(input_image)

        if len(input_image.shape)==2:
            input_image = np.expand_dims(input_image, -1)

        nodule_images = np.zeros(input_image.shape)

        for j in range(input_image.shape[-1]):
            boxes = self.data['boxes'][j]['corners']
            # no spacing info in GC with 3D version
            #x_min, y_min, x_max, y_max = boxes[2][0]/spacing_x, boxes[2][1]/spacing_y, boxes[0][0]/spacing_x, boxes[0][1]/spacing_y
            x_min, y_min, x_max, y_max = boxes[2][0], boxes[2][1], boxes[0][0], boxes[0][1]

            x_min, y_min, x_max, y_max = int(x_min), int(y_min), int(x_max), int(y_max)

            #------------------------------ Randomly choose ct patch and scale it according to bounding box size.
            ct_path = '1.3.6.1.4.1.14519.5.2.1.6279.6001.100621383016233746780170740405_dcm_1.mha'
            seg_path = '1.3.6.1.4.1.14519.5.2.1.6279.6001.100621383016233746780170740405_seg_1.mha'
            nodule_patch = self.process_CT_patches(ct_path, seg_path, (max(x_max-x_min, y_max-y_min)))
            

            cxr_img = input_image[:,:,j]
            # scale between 0 to 255.
            cxr_img_scaled = ((cxr_img - cxr_img.min()) * (1/(cxr_img.max() - cxr_img.min()) * 255)).astype('uint8')
            # this is not always a good strategy! arbitrary location
            max_value, min_value = np.max(cxr_img_scaled[730:750, 500:520]), np.min(cxr_img_scaled[730:750, 500:520])
            
            nodule_patch_scaled = ((nodule_patch - nodule_patch.min()) * (1/(nodule_patch.max() - nodule_patch.min()) * (max_value-min_value))+min_value).astype('uint8')

            bb_x_size, bb_y_size = (x_max-x_min), (y_max-y_min)
            extra_area = int((nodule_patch_scaled.shape[0]-bb_x_size)/2)
            extra_area_y = int((nodule_patch_scaled.shape[1]-bb_y_size)/2)

            crop = cxr_img_scaled[x_min-extra_area:x_min-extra_area+nodule_patch_scaled.shape[0], y_min-extra_area_y:y_min-extra_area_y+nodule_patch_scaled.shape[1]]
            # indexes where 2d fake nodule image (CT-generated) is not black
            indexes = nodule_patch_scaled!=np.min(nodule_patch_scaled)
            # if not black, average it with background.
            nodule_patch_scaled[indexes] = np.mean(np.array([crop[indexes], nodule_patch_scaled[indexes]]), axis=0) 
            # otherwise use the pixel values from the original image.
            nodule_patch_scaled[~indexes]=crop[~indexes]
            # blend the nodule data to CXR image
            cxr_img_scaled[x_min-extra_area:x_min-extra_area+nodule_patch_scaled.shape[0], y_min-extra_area_y:y_min-extra_area_y+nodule_patch_scaled.shape[1]] = nodule_patch_scaled
            nodule_images[:,:,j] = cxr_img_scaled 
           
            return SimpleITK.GetImageFromArray(nodule_images)

if __name__ == "__main__":
    Nodulegeneration().process()
