FROM python:3.7-slim

RUN groupadd -r algorithm && useradd -m --no-log-init -r -g algorithm algorithm

RUN mkdir -p /opt/algorithm /input /output \
    && chown algorithm:algorithm /opt/algorithm /input /output

USER algorithm

WORKDIR /opt/algorithm

ENV PATH="/home/algorithm/.local/bin:${PATH}"

RUN python -m pip install --user -U pip

COPY --chown=algorithm:algorithm nodule_patch/1.3.6.1.4.1.14519.5.2.1.6279.6001.100621383016233746780170740405_dcm_1.mha /opt/algorithm/1.3.6.1.4.1.14519.5.2.1.6279.6001.100621383016233746780170740405_dcm_1.mha

COPY --chown=algorithm:algorithm nodule_patch/1.3.6.1.4.1.14519.5.2.1.6279.6001.100621383016233746780170740405_seg_1.mha /opt/algorithm/1.3.6.1.4.1.14519.5.2.1.6279.6001.100621383016233746780170740405_seg_1.mha

COPY --chown=algorithm:algorithm requirements.txt /opt/algorithm/
COPY --chown=algorithm:algorithm utils.py /opt/algorithm/

RUN python -m pip install --user -rrequirements.txt

COPY --chown=algorithm:algorithm process.py /opt/algorithm/

ENTRYPOINT python -m process $0 $@

## ALGORITHM LABELS ##

# These labels are required
LABEL nl.diagnijmegen.rse.algorithm.name=nodulegeneration

# These labels are required and describe what kind of hardware your algorithm requires to run.
LABEL nl.diagnijmegen.rse.algorithm.hardware.cpu.count=4
LABEL nl.diagnijmegen.rse.algorithm.hardware.cpu.capabilities=()
LABEL nl.diagnijmegen.rse.algorithm.hardware.memory=40G
LABEL nl.diagnijmegen.rse.algorithm.hardware.gpu.count=1
LABEL nl.diagnijmegen.rse.algorithm.hardware.gpu.cuda_compute_capability=
LABEL nl.diagnijmegen.rse.algorithm.hardware.gpu.memory=11G


