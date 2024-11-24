#!/bin/sh

source .venv/bin/activate

gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app