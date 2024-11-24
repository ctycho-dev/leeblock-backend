#!/bin/sh

docker-compose down

git pull origin main

docker build . -t leeblock_fastapi

docker-compose up -d
