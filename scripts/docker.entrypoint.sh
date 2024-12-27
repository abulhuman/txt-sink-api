#!/usr/bin/env bash

set -e

cd /app

RUN_MANAGE_PY='/root/.local/bin/poetry run python -m src.manage'

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

echo 'Creating superuser...'
DJANGO_SUPERUSER_PASSWORD=$TXT_SINK_SETTINGS_DJANGO_SUPERUSER_PASSWORD $RUN_MANAGE_PY createsuperuser --no-input \
--username $TXT_SINK_SETTINGS_DJANGO_SUPERUSER_USERNAME --email $TXT_SINK_SETTINGS_DJANGO_SUPERUSER_EMAIL || echo 'Superuser already exists.'

exec /root/.local/bin/poetry run gunicorn src.core.asgi:application -k uvicorn_worker.UvicornWorker -b :$TXT_SINK_SETTINGS_GUNICORN_PORT

