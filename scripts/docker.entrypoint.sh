#!/usr/bin/env bash

set -e

cd /app
/root/.local/bin/poetry run python3 -m pip install uvicorn-worker

RUN_MANAGE_PY='/root/.local/bin/poetry run python -m src.manage'

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

echo 'Creating superuser...'
$RUN_MANAGE_PY createsuperuser --no-input || echo 'Superuser already exists.'

exec make deploy
