#FROM pytorch/pytorch
FROM python:3.7-slim

RUN groupadd -r algorithm && useradd -m --no-log-init -r -g algorithm algorithm

RUN mkdir -p /opt/algorithm /input /output \
    && chown algorithm:algorithm /opt/algorithm /input /output

USER algorithm

WORKDIR /opt/algorithm

ENV PATH="/home/algorithm/.local/bin:${PATH}"

RUN python -m pip install --user -U pip
RUN  pip install --upgrade pip

COPY --chown=algorithm:algorithm requirements.txt /opt/algorithm/
COPY --chown=algorithm:algorithm entrypoint.sh /opt/algorithm/

COPY --chown=algorithm:algorithm model /opt/algorithm/
COPY --chown=algorithm:algorithm resnet50-19c8e357.pth  /home/algorithm/.cache/torch/hub/checkpoints/resnet50-19c8e357.pth
COPY --chown=algorithm:algorithm training_utils /opt/algorithm/training_utils


RUN python -m pip install --user -rrequirements.txt

COPY --chown=algorithm:algorithm process.py /opt/algorithm/


ENTRYPOINT ["bash", "entrypoint.sh"]

## ALGORITHM LABELS ##
LABEL nl.diagnijmegen.rse.algorithm.name=noduledetection
# These labels are required and describe what kind of hardware your algorithm requires to run for grand-challenge.
LABEL nl.diagnijmegen.rse.algorithm.hardware.cpu.count=2
LABEL nl.diagnijmegen.rse.algorithm.hardware.cpu.capabilities=()
LABEL nl.diagnijmegen.rse.algorithm.hardware.memory=12G
LABEL nl.diagnijmegen.rse.algorithm.hardware.gpu.count=1
LABEL nl.diagnijmegen.rse.algorithm.hardware.gpu.cuda_compute_capability=
LABEL nl.diagnijmegen.rse.algorithm.hardware.gpu.memory=10G


