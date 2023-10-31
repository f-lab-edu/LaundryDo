#!/bin/bash
set -eu

alembic upgrade head
HOST=${HOST:-"0.0.0.0"}
PORT=${PORT:-8000}
WORKERS=${WORKERS:-1}
APP_NAME=${APP_NAME:-"src.infrastructure.api.app:app"}
uvicorn ${APP_NAME} \
    --host ${HOST} \
    --port ${PORT} \
    --workers ${WORKERS} \
    --reload