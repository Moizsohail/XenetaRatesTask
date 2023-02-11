FROM python:3.8-slim as base

RUN pip install pytest
RUN pip install pytest-watch

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN python --version ; pip --version

WORKDIR backend/src

ENTRYPOINT ["ptw","--","-rx"]