#!/usr/bin/env bash

set -e

cd /app

RUN_MANAGE_PY='/root/.local/bin/poetry run python -m src.manage'

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

echo 'Collecting static files...'
$RUN_MANAGE_PY collectstatic --no-input

echo 'Creating superuser...'
DJANGO_SUPERUSER_PASSWORD=$TXT_SINK_SETTINGS_DJANGO_SUPERUSER_PASSWORD $RUN_MANAGE_PY createsuperuser --no-input \
--username $TXT_SINK_SETTINGS_DJANGO_SUPERUSER_USERNAME --email $TXT_SINK_SETTINGS_DJANGO_SUPERUSER_EMAIL || echo 'Superuser already exists.'

echo "Fetching IP addresses..."
HOST_IPS=$(hostname -I)
IFS=' ' read -r -a HOST_IP_ARRAY <<< "$HOST_IPS"

# Remove the initial and final square brackets from TXT_SINK_SETTINGS_ALLOWED_HOSTS
TXT_SINK_SETTINGS_ALLOWED_HOSTS=${TXT_SINK_SETTINGS_ALLOWED_HOSTS:1:-1}

# surround each element with single quotes
TXT_SINK_SETTINGS_ALLOWED_HOSTS=$(echo $TXT_SINK_SETTINGS_ALLOWED_HOSTS | sed "s/,/','/g")

ALLOWED_HOSTS="['${TXT_SINK_SETTINGS_ALLOWED_HOSTS//,/','}'"
for HOST_IP in "${HOST_IP_ARRAY[@]}"; do
  ALLOWED_HOSTS="$ALLOWED_HOSTS, '$HOST_IP'"
done

# Append CIDR range 10.0.10.0/24 and range 10.0.11.0/24
for i in {0..255}; do
  ALLOWED_HOSTS="$ALLOWED_HOSTS, '10.0.10.$i'"
  ALLOWED_HOSTS="$ALLOWED_HOSTS, '10.0.11.$i'"
done

ALLOWED_HOSTS="$ALLOWED_HOSTS]"

# Export ALLOWED_HOSTS
export ALLOWED_HOSTS

echo "Updated ALLOWED_HOSTS#Count=${#ALLOWED_HOSTS}"

# Pass environment variable to Gunicorn
TXT_SINK_SETTINGS_ALLOWED_HOSTS="$ALLOWED_HOSTS" SECRET_KEY="$TXT_SINK_SETTINGS_SECRET_KEY" exec  /root/.local/bin/poetry run gunicorn src.core.asgi:application -k uvicorn_worker.UvicornWorker -b :$TXT_SINK_SETTINGS_GUNICORN_PORT


