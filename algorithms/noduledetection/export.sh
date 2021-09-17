#!/usr/bin/env bash

./build.sh

docker save detector | gzip -c > noduledetection.tar.gz
