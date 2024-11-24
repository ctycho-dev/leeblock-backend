#!/bin/sh

docker-copmose down

git pull origin main

dcoker build . -t leeblock_fastapi

docker-copmose up -d
