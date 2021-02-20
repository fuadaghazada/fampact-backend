#!/bin/sh

set -e

if [ $1 = "PROD" ]; then
  docker-compose -f docker-compose.prod.yml up --build -d
fi

if [ $1 = "DEV" ]; then
  docker-compose up --build
fi

if [ $1 = "DEV2" ]; then
  docker-compose -f docker-compose.prod.yml up --build
fi