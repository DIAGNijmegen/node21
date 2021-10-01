![alt text](https://github.com/DIAGNijmegen/node21/blob/main/images/node21.PNG)

This repository contains code related to the [NODE21](https://node21.grand-challenge.org/) challenge.  There are two main components included here:
* [**algorithms:**](https://github.com/DIAGNijmegen/node21/tree/main/algorithms/) sample code to demonstrate how to create a submission to the challenge.
* [**evaluation:**](https://github.com/DIAGNijmegen/node21/tree/main/evaluation/) organizer's code for the evaluation of submitted algorithms.

If you are (or would like to be) a participant in the challenge you are strongly advised to clone this repository as described below
and then head to the [algorithms](https://github.com/DIAGNijmegen/node21/tree/main/algorithms/) section to understand how to make your submission.

If you are just curious to see how evaluation is implemented then feel free to browse around [the evaluation code](https://github.com/DIAGNijmegen/node21/tree/main/evaluation/)

## Prerequisites
* [Docker](https://www.docker.com/get-started)
* [evalutils](https://github.com/comic/evalutils)

The code in this repository is based on docker and evalutils.  

**Windows Tip**: For participants using Windows, it is highly recommended to 
install [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/install-win10) 
to work with Docker on a Linux environment within Windows. Please make sure to install **WSL 2** by following the instructions on the same page. 
The alternative is to work purely out of Ubuntu, or any other flavor of Linux.
Also, note that the basic version of WSL 2 does not come with GPU support. 
Please watch the [official tutorial](https://www.youtube.com/watch?v=PdxXlZJiuxA) 
by Microsoft on installing WSL 2 with GPU support.

Please clone the repository as follows:
```python
git clone https://github.com/DIAGNijmegen/node21.git
```









