FROM python:3.8-alpine
MAINTAINER FamPact
ENV PYTHONUNBUFFERED 1

# Requirements
COPY ./requirements/base-requirements.txt /base-requirements.txt
COPY ./requirements/dev-requirements.txt /requirements.txt

# Temp. Dependencies
RUN apk add --update --no-cache postgresql-client
RUN apk add --no-cache gettext
RUN apk add --no-cache libjpeg
RUN apk add --update --no-cache --virtual .tmp-build-deps \
    gcc libc-dev linux-headers postgresql-dev \
    build-base postgresql libpq jpeg-dev zlib-dev \
    libressl-dev musl-dev libffi-dev

# Installing the dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Deleting temp. dependencies
RUN apk del .tmp-build-deps

# Creating app directory
RUN mkdir /app
WORKDIR /app
COPY ./app .app

# User
RUN adduser -D user
USER user