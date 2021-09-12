# Nodule Detection Algorithm

This codebase implements a simple baseline model for nodule detection track in [NODE21](https://node21.grand-challenge.org/). It contains all necessary files to build a docker image from in order to help the participants to create their own algorithm for submission to [NODE21](https://node21.grand-challenge.org/) detection track. 

For serving this algorithm in a docker container compatible with the requirements of grand-challenge, we used [evalutils](https://github.com/comic/evalutils) which provides methods to wrap your algorithm in Docker containers. It automatically generates template scripts for your container files, and creates commands for building, testing, and exporting the algorithm container. We adapted this template code for our algorithm by following the [tutorial](https://grand-challenge.org/blogs/create-an-algorithm/). For learning how to use evalutils, and how to adapt it for your own algorithm, we refer you to the [tutorial](https://grand-challenge.org/blogs/create-an-algorithm/). The details regarding how NODE21 detection algorithm is expected to work is described below.

##### Table of Contents  
[Prerequisites](#Prerequisites)  
[An overview of the structure of this example](#algorithm)  
[Interfaces](#interfaces)  
[Building your container](#build)  
[Testing your container](#test)  
[Export your algorithm container](#export)  

<a name="Prerequisites"/>

## Prerequisites
* [Docker](https://www.docker.com/get-started)
* [evalutils](https://github.com/comic/evalutils) 
* [git-lfs](https://github.com/git-lfs/git-lfs/wiki/Installation)

This container is based on docker and evalutils. As stated by grand-challenge team in the algorithm [tutorial](https://grand-challenge.org/blogs/create-an-algorithm/), for participants using Windows, it is highly recommended to install Windows Subsystem for Linux (WSL) to work with Docker on a Linux environment within Windows. Please make sure to install **WSL 2** by following the instructions on the same page. The alternative is to work purely out of Ubuntu, or any other flavor of Linux.

Installation of git-lfs is required to pull the model weights for the nodule detection algorithm (noduledetection/model). 

Please clone the repository as follows:
```python
git clone https://github.com/DIAGNijmegen/node21.git
```

In order to pull the model weights for the nodule detection algorithm, please run the following command:

```python
git lfs pull noduledetection/model
```

<a name="interfaces"/>

## Input and output interfaces
The nodule detection algorithm takes as input a chest X-ray (CXR) and outputs a nodules.json file. It reads the input :
* CXR at "/input/<uuid>.mha"
  
 and writes the output to
* nodules.json file at "/output/nodules.json".

Nodules.json file contains the predicted bounding box locations per image. This file contains multiple 2D bounding boxes coordinates in [CIRRUS](https://comic.github.io/grand-challenge.org/components.html#grandchallenge.components.models.InterfaceKind.interface_type_annotation) compatible format, an example json file is as follows:
```python
{
    "type": "Multiple 2D bounding boxes",
    "boxes": [
        {
        "corners": [
            [ 92.66666412353516, 136.06668090820312, 0],
            [ 54.79999923706055, 136.06668090820312, 0],
            [ 54.79999923706055, 95.53333282470703, 0],
            [ 92.66666412353516, 95.53333282470703, 0]
        ]
        probability=0.6
        },
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
```
### Operating on a 3D image

For the sake of time effeciency in the evaluation process of [NODE21](https://node21.grand-challenge.org/), the submitted algorithms to [NODE21](https://node21.grand-challenge.org/) are expected to operate on a 3D image where multiple CXR images are stacked together. This means that, the algorithms should handle 3D image, by reading a CXR slice by slice. The third coordinate of the bounding box in nodules.json file are used as an identifier of the CXR. If the algorithm processes the first CXR image in 3D volume, the z coordinate would be 0, if it processes the third CXR image, it would be 2.

<a name="build"/>

### Building and testing the docker

Run the following command to build the docker:
docker build -t nodulegenerator .

To test the docker container, run the following command (map /input to your own test directory):
docker run --rm --memory=11g -v small_test/:/input/ -v nodulegeneration-output:/output/ nodulegenerator

To save the container, run the following command:
docker save nodulegenerator | gzip -c > nodulegeneration.tar.gz
    
    
 ### Submit your algorithm
 Participants should first upload their algorithm by creating an algorithm on grand-challenge. Please go to the [link](https://grand-challenge.org/algorithms/create/) to create an algorithm as follows:
    




