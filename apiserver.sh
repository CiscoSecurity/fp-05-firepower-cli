#!/bin/bash

DIR=/ocsf/fp-05-firepower-cli/fastapi/
WORKERS=4
WORKER_CLASS=uvicorn.workers.UvicornWorker
HOST=0.0.0.0
PORT=8282
BIND=$HOST:$PORT
LOG_LEVEL=error

cd $DIR

exec gunicorn main:app \
  --workers $WORKERS \
  --worker-class $WORKER_CLASS \
  --bind=$BIND \
  --log-level=$LOG_LEVEL 
