# Nodule Detection Algorithm

This codebase implements a baseline model, [Faster R-CNN](https://papers.nips.cc/paper/2015/hash/14bfa6bb14875e45bba028a21ed38046-Abstract.html), for nodule detection track in [NODE21](https://node21.grand-challenge.org/). It contains all necessary files to build a docker image from in order to help the participants to create their own algorithm for submission to [NODE21](https://node21.grand-challenge.org/) detection track. 

For serving this algorithm in a docker container compatible with the requirements of grand-challenge, we used [evalutils](https://github.com/comic/evalutils) which provides methods to wrap your algorithm in Docker containers. It automatically generates template scripts for your container files, and creates commands for building, testing, and exporting the algorithm container. We adapted this template code for our algorithm by following the [tutorial](https://grand-challenge.org/blogs/create-an-algorithm/). For learning how to use evalutils, and how to adapt it for your own algorithm, we refer you to the [tutorial](https://grand-challenge.org/blogs/create-an-algorithm/). The details regarding how NODE21 detection algorithm is expected to work is described below.

##### Table of Contents  
[An overview of the baseline algorithm](#algorithm)  
[Configuring the Docker File](#dockerfile)
[Building your container](#build)  
[Testing your container](#test)  
[Export your algorithm container](#export)  

<a name="algorithm"/>

## An overview of the baseline algorithm
The baseline nodule detection algorithm is a [Faster R-CNN](https://papers.nips.cc/paper/2015/hash/14bfa6bb14875e45bba028a21ed38046-Abstract.html) model, which was implemented using [pytorch](https://pytorch.org/) library. The main file executed by the docker container is [*process.py*](https://github.com/DIAGNijmegen/node21/blob/main/algorithms/noduledetection/process.py). 


### Input and Output Interfaces
It takes as input a chest X-ray (CXR) and outputs a nodules.json file. It reads the input :
* CXR at ``` "/input/<uuid>.mha"```
  
 and writes the output to
* nodules.json file at ``` "/output/nodules.json".```

Nodules.json file contains the predicted bounding box locations associated with the probability (likelihood). This file is a dictionary and contains multiple 2D bounding boxes coordinates in [CIRRUS](https://comic.github.io/grand-challenge.org/components.html#grandchallenge.components.models.InterfaceKind.interface_type_annotation) compatible format, an example json file is as follows:
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
The coordinates are expected in milimiters when spacing information is available. We provide a [function](https://github.com/DIAGNijmegen/node21/blob/main/algorithms/noduledetection/process.py#L121) in [*process.py*](https://github.com/DIAGNijmegen/node21/blob/main/algorithms/noduledetection/process.py) which converts the predictions of Faster R-CNN model to this format. 

### Operating on a 3D image

For the sake of time effeciency in the evaluation process of [NODE21](https://node21.grand-challenge.org/), the submitted algorithms to [NODE21](https://node21.grand-challenge.org/) are expected to operate on a 3D image where multiple CXR images are stacked together. This means that, the algorithms should handle 3D image, by reading a CXR slice by slice. The third coordinate of the bounding box in nodules.json file are used as an identifier of the CXR. If the algorithm processes the first CXR image in 3D volume, the z coordinate would be 0, if it processes the third CXR image, it would be 2.

<a name="build"/>
  
### Running the container in multiple phases:
The container images submitted to NODE21 detection track should have the possibility of running in four different phases:
1. ```no arguments``` given (test phase): Load the 'model' file, and test the model on a given image. This is the default mode.
2. ```--train``` phase: Train the model from scratch given the folder with training images and metadata.csv. Save the model frequently as model_retrained.
3. ```--retrain``` phase: Load the (pretrained) 'model' file, and retrain the model given the folder with training images and metadata.csv. Save the model frequently as model_retrained.
4. ```--retest``` phase: Load 'model_retrain' which was created during the training phase, and test it on a given image.
  
This sounds like too many different phases and looks complicated, but it is not, no worries! This is simply implemented in process.py, and we will walk you though the details of those phases. At the end, you will only need to create a training phase, and all other phases are tiny modifications of the train and test phases. 

As seen in the 'process.py' file, the phase of a docker image is determined by the command line arguments given while running the docker image. If no argument is given, the docker image will run in test phase by default (grand-challenge will run the submitted algorithms in test phase).
  
Selected detection solutions will be run on train and evaluate phase for the overview challenge paper for various experiments. Participants whose solutions are selected will be invited to be the co-author of the overview challenge paper. 
  
Important NOTE: in case the selected solutions cannot be run in the training phase, the participants will be contacted ***for one time only*** to fix their docker image. If the solution is not fixed on time, we will have to exclude their solutions and they will not be eligible for the authorship in the overview paper.
  
  
should have additonal training phase. We asked the participants to create the docker image with the training option as well as this will be used in case the solution of the participants is selected, and they are invited to be co-author of the challenge overview paper. If the docker images cannot be run in training phase, the participants will be contacted to fix their solution after the challenge deadline, and in case of no colloboration, the participants will not be included 

<a name="dockerfile"/>

### Configure the Docker file
We recommend that you use our [dockerfile](https://github.com/DIAGNijmegen/node21/blob/main/algorithms/noduledetection/Dockerfile) as reference, and update it according to your algorithm requirements. There are three main components you need to define in your docker file in order to wrap your algorithm in a docker container:
1. Choose the right base image (official base image from the library you need (tensorflow, pytorch etc.) recommended)
```python
FROM pytorch/pytorch:1.9.0-cuda11.1-cudnn8-runtime
```
3. Copy all the files you need to run your model : model weights, *requirement.txt*, all the python files you need etc.
```python
COPY --chown=algorithm:algorithm requirements.txt /opt/algorithm/
COPY --chown=algorithm:algorithm entrypoint.sh /opt/algorithm/
COPY --chown=algorithm:algorithm model /opt/algorithm/
COPY --chown=algorithm:algorithm resnet50-19c8e357.pth  /home/algorithm/.cache/torch/hub/checkpoints/resnet50-19c8e357.pth
COPY --chown=algorithm:algorithm training_utils /opt/algorithm/training_utils
```

5. Install all the dependencies, defined in *reqirements.txt*, in your dockerfile.
```python
RUN python -m pip install --user -rrequirements.txt
```
Ensure that all of the dependencies with their versions are specified in requirements.txt:
```
evalutils==0.2.4
scikit-learn==0.20.2
scipy==1.2.1
--find-links https://download.pytorch.org/whl/torch_stable.html 
torchvision==0.10.0+cu111 
torchaudio==0.9.0
scikit-image==0.17.2
```
### Building and testing the docker

Run the following command to build the docker:
 ```python
docker build -t noduledetector .
 ```

To test the docker container, run the following command (map /input to your own test directory):
 ```python
 docker run --rm --memory=11g -v small_test/:/input/ -v nodulegeneration-output:/output/ noduledetector
 ```

To save the container, run the following command:
 ```python
  docker save noduledetector | gzip -c > noduledetector.tar.gz
 ```
    
    
 ### Submit your algorithm
 Once you have your docker image ready (.tar.gz file), you are ready to submit! Let us walk you through the steps you need to follow to upload and submit your algorithm to [NODE21](https://node21.grand-challenge.org/) detection track:

1. In order to submit your docker container, you first have to create an algorithm entry for your docker container [here](https://grand-challenge.org/algorithms/create/).
   * Please choose a title for your algorithm and add a (squared image) logo. Enter the modalities and structure information as in the example below.
      ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/algorithm_description.PNG)

    * Scrolling down the page, you will see that you need to enter the information regarding the interface of the algorithm. Please select *Generic Medical Image (Image)* as Inputs, and *Nodules (Multiple 2D Bounding Boxes)* as Outputs. Do not forget to pick the workstation as *Viewer CIRRUS Core (Public)*. 
      ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/algorithm_interfaces.PNG)
  
2. After saving it, you are ready to upload your docker container. Choose the container tab, and upload your container. You can also overwrite your container by uploading a new one. That means that when you make changes to your algorithm, you could overwrite your container and submit the updated version of your algorithm to node21:
    ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/algorithm_uploadcontainer.PNG)

3. OPTIONAL: Please note that it can take a while (several minutes) until the container becomes active. Once it becomes active, we suggest that you try out the algorithm to verify everything works as expected. For this, please click on *Try-out Algorithm* tab, and upload a *Generic Medical Image*. You could upload the image in the test folder since it is a 3D image (CXRs are stacked together), and test data would be in the same format.
  ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/algorithm_tryout.PNG)
4. OPTIONAL: You could look at the results of your algorithm: click on the *Results*, and *Open Result in Viewer* to visualize the results. You would be directed to CIRRUS viewer, and the results will be visualized with the predicted bounding boxes on chest x-ray images as below. You could move to the next and previous slice (slice is a chest x-ray in this case) by clicking on the up and down arrow in the keyboard.
    ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/algorithm_results.PNG)

5. Go to the [NODE21](https://node21.grand-challenge.org/evaluation/challenge/submissions/create/) submission page, and submit your solution to the detection track by choosing your algorithm.
   ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/node21_submission.PNG)
    




