# Nodule Generation Algorithm

This codebase implements a baseline model for nodule generation track in [NODE21](https://node21.grand-challenge.org/). For serving this algorithm in a docker container compatible with the requirements of grand-challenge, we followed the [tutorial](https://grand-challenge.org/blogs/create-an-algorithm/). 

## Input and output interfaces

The nodule generation algorithm takes as input a chest X-ray (CXR) and a nodules.json file and produces a CXR after placing nodules at given locations. It reads the input :
* CXR at "/input/<uuid>.mha"
* nodules.json file at "/input/nodules.json".

Nodules.json file determines where nodules should be placed on a given CXR. This file contains multiple 2D bounding boxes coordinates in [CIRRUS](https://comic.github.io/grand-challenge.org/components.html#grandchallenge.components.models.InterfaceKind.interface_type_annotation) compatible format, an example json file is as follows:

{
    "type": "Multiple 2D bounding boxes",
    "boxes": [
        {
        "corners": [
            [ 92.66666412353516, 136.06668090820312, 0],
            [ 54.79999923706055, 136.06668090820312, 0],
            [ 54.79999923706055, 95.53333282470703, 0],
            [ 92.66666412353516, 95.53333282470703, 0]
        ]},
        {
        "corners": [
            [ 92.66666412353516, 136.06668090820312, 0],
            [ 54.79999923706055, 136.06668090820312, 0],
            [ 54.79999923706055, 95.53333282470703, 0],
            [ 92.66666412353516, 95.53333282470703, 0]
        ]}
    ],
    "version": { "major": 1, "minor": 0 }
}

### Operating on a 3D image

For the sake of time effeciency in the evaluation process of [NODE21](https://node21.grand-challenge.org/), the submitted algorithms to [NODE21](https://node21.grand-challenge.org/) are expected to operate on a 3D image where multiple CXR images are stacked together. This means that, the algorithms should handle 3D image, by reading a CXR slice by slice. The third coordinate of the bounding box in nodules.json file are used as an identifier of the CXR. If the algorithm processes the first CXR image in 3D volume, the z coordinate would be 0, if it processes the third CXR image, it would be 2.


### Building and testing the docker

Run the following command to build the docker:
docker build -t nodulegenerator .

To test the docker container, run the following command (map /input to your own test directory):
docker run --rm --memory=11g -v small_test/:/input/ -v nodulegeneration-output:/output/ nodulegenerator

To save the container, run the following command:
docker save nodulegenerator | gzip -c > nodulegeneration.tar.gz




