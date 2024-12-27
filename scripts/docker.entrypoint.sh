#!/usr/bin/env bash

set -e

cd /app

RUN_MANAGE_PY='/root/.local/bin/poetry run python -m src.manage'

echo "[DEBUG] printing ALLOWED_HOSTS"
echo  "ALLOWED_HOSTS=$ALLOWED_HOSTS"
echo  "TXT_SINK_SETTINGS_ALLOWED_HOSTS=$TXT_SINK_SETTINGS_ALLOWED_HOSTS"
echo "[DEBUG] end printing ALLOWED_HOSTS"

echo '[DEBUG] printing DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD'
echo "DJANGO_SUPERUSER_USERNAME=$DJANGO_SUPERUSER_USERNAME"
echo "DJANGO_SUPERUSER_PASSWORD=$DJANGO_SUPERUSER_PASSWORD"
echo '[DEBUG] end printing DJANGO_SUPERUSER_USERNAME and DJANGO_SUPERUSER_PASSWORD'

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

echo 'Creating superuser...'
DJANGO_SUPERUSER_PASSWORD=$TXT_SINK_SETTINGS_DJANGO_SUPERUSER_PASSWORD $RUN_MANAGE_PY createsuperuser --no-input \
--username $TXT_SINK_SETTINGS_DJANGO_SUPERUSER_USERNAME --email $TXT_SINK_SETTINGS_DJANGO_SUPERUSER_EMAIL || echo 'Superuser already exists.'

exec /root/.local/bin/poetry run gunicorn src.core.asgi:application -k uvicorn_worker.UvicornWorker -b :$GUNICORN_PORT

