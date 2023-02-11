FROM python:3.8-slim as base


COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
RUN python --version ; pip --version

WORKDIR backend