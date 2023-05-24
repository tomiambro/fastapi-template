#! /usr/bin/env bash
set -e

python /app/app/initialize-celery.py

celery -A app.tasks.celery_scheduler beat -l debug
