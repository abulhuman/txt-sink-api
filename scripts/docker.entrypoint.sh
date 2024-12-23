#!/usr/bin/env bash

set -e

RUN_MANAGE_PY='poetry run python -m src.manage'

echo 'Running migrations...'
$RUN_MANAGE_PY migrate --no-input

make deploy
