#!/usr/bin/env bash

SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"

./build.sh

docker volume create eval-output

docker run --rm \
        --memory=4g \
        -v $SCRIPTPATH/test/:/input/ \
        -v eval-output:/output/ \
        evaluation_detection

docker run --rm \
        -v eval-output:/output/ \
        python:3.7-slim cat /output/metrics.json | python -m json.tool

docker volume rm eval-output
