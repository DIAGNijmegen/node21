# Nodule Generation Algorithm

This codebase implements a simple baseline model following the main steps in the [paper](https://geertlitjens.nl/publication/litj-10-a/litj-10-a.pdf) published by Litjens et al., for nodule generation track in [NODE21](https://node21.grand-challenge.org/). It contains all necessary files to build a docker image from in order to help the participants to create their own algorithm for submission to the generation track. 

For serving this algorithm in a docker container compatible with the requirements of grand-challenge, we used [evalutils](https://github.com/comic/evalutils) which provides methods to wrap your algorithm in Docker containers. It automatically generates template scripts for your container files, and creates commands for building, testing, and exporting the algorithm container. We adapted this template code for our algorithm by following the [tutorial](https://grand-challenge.org/blogs/create-an-algorithm/). For learning how to use evalutils, and how to adapt it for your own algorithm, we refer you to the [tutorial](https://grand-challenge.org/blogs/create-an-algorithm/). The details regarding how NODE21 generation algorithm is expected to work is described below.

##### Table of Contents  
[An overview of the structure of this example](#algorithm)  
[Interfaces](#interfaces)  
[Building your container](#build)  
[Testing your container](#test)  
[Export your algorithm container](#export)

<a name="interfaces"/>

## Input and output interfaces
The nodule generation algorithm takes as input a chest X-ray (CXR) and a nodules.json file and produces a CXR after placing nodules at given locations. It reads the input :
* CXR at ```"/input/<uuid>.mha"```
* nodules.json file at ```"/input/nodules.json"```.

*Nodules.json* file provides information of where nodules should be placed on a given CXR. This file contains multiple 2D bounding boxes coordinates in [CIRRUS](https://comic.github.io/grand-challenge.org/components.html#grandchallenge.components.models.InterfaceKind.interface_type_annotation) compatible format, an example json file is as follows:

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
```

The algorithm reads the inputs (a medical image and *nodules.json*) and produces an image with a generated nodule at the requested location (provided with nodules.json). The resulting image is written to /output/.

📌 NOTE: In order to run this codebase, nodule_patches folder should contain all the ct nodule patches and corresponding segmentation maps, which are provided in zenodo release of NODE21. If you would like to run this algorithm, please copy all the provided ct nodule patches and segmentations inside nodule_patches folder. 

💡 To test this container locally without a docker container, you should the execute_in_docker flag to False - this sets all paths to relative paths. You should set it back to True when you want to switch back to the docker container setting.

### Operating on a 3D image
For the sake of time effeciency in the evaluation process of [NODE21](https://node21.grand-challenge.org/), the submitted algorithms to [NODE21](https://node21.grand-challenge.org/) are expected to operate on a 3D image where multiple CXR images are stacked together. This means that, the algorithms should handle 3D image, by reading a CXR slice by slice. The third coordinate of the bounding box in nodules.json file are used as an identifier of the CXR. If the algorithm processes the first CXR image in 3D volume, the z coordinate would be 0, if it processes the third CXR image, it would be 2.


### Build, test and export your container
1. To test if all dependencies are met, you could run the file build.bat (Windows) / build.sh (Linux) to build the docker container. Please note that the next step (testing the container) also runs a build, so this step is not necessary if you are certain that everything is set up correctly.
    
    *build.sh*/*build.bat* files will run the following command to build the docker for you:
    ```python 
    docker build -t nodulegenerator .
    ```

2. To test the docker container to see if it works as expected, *test.sh*/*test.bat* will run the container on images provided in  ```test/``` folder, and it will check the results (*results.json* produced by your algorithm) against ```test/expected_output.json```. 
    
    Once you validated that the algorithm works as expected, you might want to simply run the algorithm on the test folder and check nodules.json file (see $SCRIPTPATH/results/), you could use the following command for this: 
   ```python
   docker run --rm --memory=11g -v path_to_your_test_folder/:/input/ -v path_to_your_output_folder/:/output/ nodulegenerator
   ```
   
  
3. Run *export.sh*/*export.bat* to save the container which run the following command:
   ```python
    docker save nodulegenerator | gzip -c > nodulegenerator.tar.gz
   ```
    
    
 ### Submit your algorithm
 Once you have your docker image ready (.tar.gz file), you are ready to submit! Let us walk you through the steps you need to follow to upload and submit your algorithm to [NODE21](https://node21.grand-challenge.org/) generation track:

1. In order to submit your docker container, you first have to create an algorithm entry for your docker container [here](https://grand-challenge.org/algorithms/create/).
   * Please choose a title for your algorithm and add a (squared image) logo. Enter the modalities and structure information as in the example below.
      ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/gen_algorithm_description.PNG)

    * Scrolling down the page, you will see that you need to enter the information regarding the interface of the algorithm. Please select *Generic Medical Image (Image)* and *Nodules (Multiple 2D Bounding Boxes)* as Inputs and *Generic Medical Image (Image)* as Outputs. Do not forget to pick the workstation as *Viewer CIRRUS Core (Public)*. 
      ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/gen_algorithm_interfaces.PNG)
  
2. After saving it, you are ready to upload your docker container. Choose the container tab, and upload your container. You can also overwrite your container by uploading a new one. That means that when you make changes to your algorithm, you could overwrite your container and submit the updated version of your algorithm to node21:
    ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/gen_algorithm_uploadcontainer.PNG)

3. OPTIONAL: Please note that it can take a while (several minutes) until the container becomes active. Once it becomes active, we suggest that you try out the algorithm to verify everything works as expected. For this, please click on *Try-out Algorithm* tab, and upload a *Generic Medical Image* and paste your *nodules.json* file. You could upload the image and nodules.json given in the test folder which represents how test data would look like during evaluation.
  ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/gen_algorithm_tryout.PNG)
4. OPTIONAL: You could look at the results of your algorithm: click on the *Results*, and *Open Result in Viewer* to visualize the results. You would be directed to CIRRUS viewer, and the results will be visualized with the predicted bounding boxes on chest x-ray images as below. You could move to the next and previous slice (slice is a chest x-ray in this case) by clicking on the up and down arrow in the keyboard.
    ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/gen_algorithm_results.PNG)

5. Go to the [NODE21](https://node21.grand-challenge.org/evaluation/challenge/submissions/create/) submission page, and submit your solution to the detection track by choosing your algorithm.
   ![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/node21_submission.PNG)
    





