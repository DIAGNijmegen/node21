#!/usr/bin/env bash

./build.sh

docker save evaluation_detection | gzip -c > evaluation_detection.tar.gz
