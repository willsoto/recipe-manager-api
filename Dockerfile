FROM python:latest

ENV APP_DIR /app
ENV PYTHONUNBUFFERED 1
ENV LANG en_US.UTF-8
ENV LC_ALL C.UTF-8

ADD . $APP_DIR
WORKDIR $APP_DIR

RUN pip install --upgrade pip && \
    pip install -U -e .

EXPOSE 5000
