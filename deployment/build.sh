#!/usr/bin/env bash

set -o errexit
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py collectstatic --no-input
python manage.py migrate