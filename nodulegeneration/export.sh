#!/usr/bin/env bash

./build.sh

docker save nodulegeneration | gzip -c > nodulegeneration.tar.gz
