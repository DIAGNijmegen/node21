call .\build.bat

docker volume create evaluation_detection-output

docker run --rm^
 --memory=4g^
 -v %~dp0\test\:/input/^
 -v evaluation_detection-output:/output/^
 evaluation_detection

docker run --rm^
 -v evaluation_detection-output:/output/^
 python:3.7-slim cat /output/metrics.json | python -m json.tool

docker volume rm evaluation_detection-output
