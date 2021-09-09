# NODE21

This repository contains a reference docker image implementation for both detection and generation track for the [NODE21](https://node21.grand-challenge.org/) challenge. These docker image implementations for the two tracks serve as an example algorithm submission to at [NODE21](https://node21.grand-challenge.org/) challenge. The challenge participants could use these templates to implement their own algorithm for submission. 

This additionally serves as an example of how the grand-challenge platform would expect the output of the submitted algorithms to look like. We suggest that the participants build these example docker images, and run the container image to understand the expected output of each track. Alternatively, the test folder (from detection and generation folder) contains a file called expected_output which is useful to take a look at.

For implementation of your algorithm for each track, you would need to install docker, and use evalutils (our template repository is based on evalutils template). To learn how to install docker, and use evalutils to implement a simple baseline algorithm in grand-challenge compatible format, please read the grand-challenge tutorial: [how to create an algorithm](https://grand-challenge.org/).

