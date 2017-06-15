FROM python:latest

ENV PYTHONUNBUFFERED 1
ENV LANG en_US.UTF-8
ENV LC_ALL C.UTF-8

ADD . /app
WORKDIR /app

RUN pip install --upgrade pip && \
    pip install -U -e .
