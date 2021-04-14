#!/usr/bin/env bash

./build.sh

docker save noduledetection | gzip -c > noduledetection.tar.gz
