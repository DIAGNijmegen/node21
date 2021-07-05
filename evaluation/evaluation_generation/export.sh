#!/usr/bin/env bash

./build.sh

docker save evaluation_generation | gzip -c > evaluation_generation.tar.gz
