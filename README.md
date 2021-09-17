![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/node21.PNG)

This repository contains codebase for the baseline algorithms to wrap them in a docker container and evaluation scripts to evaluate the algorithms submissions for NODE21 challenge.

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

## Baseline algorithms
[NODE21](https://node21.grand-challenge.org/) challenge only accepts algorithm submissions, which should be submitted in the form of a docker image. In order to provide a template code for the NODE21 participants, we provide baseline codes, for both detection track and generation tracks, which are implemented according to the requirements of grand-challenge.org and the requirements of NODE21 (input and output interfaces of the expected algorithm submissions).

These docker image implementations for the two tracks serve as an example algorithm submission to [NODE21](https://node21.grand-challenge.org/), and challenge participants could use these templates to implement their own algorithm. They additionally serves as an example of how the grand-challenge platform would expect the output of the submitted algorithms to look like. For implementation of your docker container algorithm for each track, you would need to install docker, and use evalutils. To learn how to install docker, and use evalutils to implement a simple baseline algorithm in grand-challenge compatible format, please read the grand-challenge tutorial: [how to create an algorithm](https://grand-challenge.org/). Our template repository is based on evalutils template, which provides methods to wrap your algorithm in Docker containers, and we made changes to implement our algorithms on top of this template. 

Pages [detection](https://github.com/DIAGNijmegen/node21/tree/main/algorithms/noduledetection) and [generation](https://github.com/DIAGNijmegen/node21/tree/main/algorithms/nodulegeneration) explains the details regarding the baseline algorithms, and will walk you through the steps to wrap your algorithm in a docker container and submission process to NODE21. Please go to the corresponding page of the track you are working ([detection](https://github.com/DIAGNijmegen/node21/tree/main/algorithms/noduledetection) or [generation](https://github.com/DIAGNijmegen/node21/tree/main/algorithms/nodulegeneration)), we encourage you to adapt this example to your needs and insert your own nodule detection or nodule generation solution. 

Lets start! 


## Evaluation of the algorithms







