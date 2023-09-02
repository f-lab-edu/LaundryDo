#!/bin/bash

# run fastapi server
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-1}
APP_NAME=${APP_NAME:-'src.infrastructure.api.app:app'}

uvicorn ${APP_NAME} \
    --host ${HOST} \
    --port ${PORT} \
    --workers ${WORKERS}
