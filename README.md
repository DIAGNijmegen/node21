# NODE21

[NODE21](https://node21.grand-challenge.org/) challenge only accepts algorithm submissions, which should be submitted in the form of a docker image. In order to provide a template code for the NODE21 participants, we provide baseline codes, for both detection track and generation tracks, which are implemented according to the requirements of grand-challenge.org and the requirements of NODE21 (input and output interfaces of the expected algorithm submissions).

These docker image implementations for the two tracks serve as an example algorithm submission to [NODE21](https://node21.grand-challenge.org/), and challenge participants could use these templates to implement their own algorithm. 

This additionally serves as an example of how the grand-challenge platform would expect the output of the submitted algorithms to look like. We suggest that the participants build these example docker images, and run the container image to understand the expected output of each track. Alternatively, the test folder (from detection and generation folder) contains a file called expected_output which is useful to take a look at.

For implementation of your algorithm submission for each track, you would need to install docker, and use evalutils. To learn how to install docker, and use evalutils to implement a simple baseline algorithm in grand-challenge compatible format, please read the grand-challenge tutorial: [how to create an algorithm](https://grand-challenge.org/). Our template repository is based on evalutils template, which provides methods to wrap your algorithm in Docker containers, and we made changes to implement our algorithms on top of evalutils template. 

Pages [detection] and [generation] explains the details regarding the baseline algorithms, and how to build, test and export the docker images. Please go to the page corresponding to the track you are working on. Once your docker image is tested (pass the test using test.sh or test.bat) and works as expected, you could upload your algorithm (exported as tar.gz) to grand challenge. 

Let us walk you through the steps you need to follow to upload your algorithm on grand-challenge, and submit the algorithm to your track:

1. please first create and algorithm and fill the extries as below.

