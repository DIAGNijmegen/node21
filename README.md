![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/node21.PNG)

Welcome to the **NODE21** page!  

Participants in the [NODE21](https://node21.grand-challenge.org/) challenge are required to make their submission 
by creating and submitting an algorithm on our [grand-challenge](https://grand-challenge.org/) platform. We additionally request that the code for your algorithm
should be available in a **public GitHub repository** with an [Apache 2.0 license](https://www.apache.org/licenses/LICENSE-2.0) present in the root folder.
You can provide the repository URL when creating your algorithm.

A general tutorial on how to create an algorithm for grand-challenge is provided
[here](https://grand-challenge.org/blogs/create-an-algorithm/). We recommend participants follow this tutorial to get an understanding of the process.

In addition to the tutorial, in this repository we provide template code for NODE21 participants for both the detection and generation tracks. These templates allow you to build working algorithms which comply with the requirements of grand-challenge and of NODE21 (specifically the input and output interfaces required for NODE21 challenge submissions). We encourage you to adapt these templates to run your own method or to model your docker image on them.

To work with the template code please first ensure you have the pre-requisites installed and have cloned this repository:

## Prerequisites
* [Docker](https://www.docker.com/get-started)
* [evalutils](https://github.com/comic/evalutils)

**Windows Tip**: For participants using Windows, it is highly recommended to 
install [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) 
to work with Docker on a Linux environment within Windows. Please make sure to install **WSL 2** by following the instructions on the same page. 
The alternative is to work purely out of Ubuntu, or any other flavor of Linux.
Also, note that the basic version of WSL 2 does not come with GPU support. 
Please watch the [official tutorial](https://www.youtube.com/watch?v=PdxXlZJiuxA) 
by Microsoft on installing WSL 2 with GPU support.

If you are working on the detection track, please clone the repository as follows:
```python
git clone https://github.com/node21challenge/node21_detection_baseline.git
```
For generation track, please clone the repository as follows:
```python
git clone https://github.com/node21challenge/node21_generation_baseline.git
```
 
Then head to the template algorithm for 
[nodule detection](https://github.com/node21challenge/node21_detection_baseline) or 
[nodule generation](https://github.com/node21challenge/node21_generation_baseline) depending on 
which track you would like to submit to.













