import os
import numpy as np
import torch
from PIL import Image
import pandas as pd

import training_utils.transforms as T

def get_transform(train):
    transforms = []
    transforms.append(T.ToTensor())
    if train:
        transforms.append(T.RandomHorizontalFlip(0.5))
    return T.Compose(transforms)

class CXRNoduleDataset(object):
    # process images from images folder.
    def __init__(self, root, csv_file, transforms):
        self.root = root
        self.transforms = transforms
        self.imgs = list(sorted(os.listdir(os.path.join(root, "images"))))
        if 'Thumbs.db' in self.imgs:
            self.imgs.remove('Thumbs.db')
        self.data = pd.read_csv(csv_file)


    def __getitem__(self, idx):
        img_path = os.path.join(self.root, "images", self.imgs[idx])
        img = Image.open(img_path)
        # simply rescale to range 0 to 1.
        img = Image.fromarray((np.asarray(img)/np.max(img)))
        nodule_data = self.data[self.data['img_name']==self.imgs[idx]]
        num_objs = len(nodule_data)
        boxes = []
        for i in range(num_objs):
            x_min = int(nodule_data.iloc[i]['x'])
            y_min = int(nodule_data.iloc[i]['y'])
            y_max = int(y_min+nodule_data.iloc[i]['height'])
            x_max = int(x_min+nodule_data.iloc[i]['width'])
            boxes.append([x_min, y_min, x_max, y_max])

        # convert everything into a torch.Tensor
        boxes = torch.as_tensor(boxes, dtype=torch.float32)
        # there is only one class which is 'nodule'
        labels = torch.ones((num_objs,), dtype=torch.int64)
        image_id = torch.tensor([idx])
        area = (boxes[:, 3] - boxes[:, 1]) * (boxes[:, 2] - boxes[:, 0])
        # suppose all instances are not crowd
        iscrowd = torch.zeros((num_objs,), dtype=torch.int64)

        target = {}
        target["boxes"] = boxes
        target["labels"] = labels
        target["image_id"] = image_id
        target["area"] = area
        target["iscrowd"] = iscrowd

        if self.transforms is not None:
            img, target = self.transforms(img, target)
        
        image_name = self.imgs[idx]

        return img, target, image_name

    def __len__(self):
        return len(self.imgs)
    
    
    
    