#!/bin/sh

git restore .
git pull origin main

docker build . -t leeblock_fastapi

docker-compose down
docker-compose up -d
