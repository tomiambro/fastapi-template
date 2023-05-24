#! /usr/bin/env bash
set -e

python /app/app/initialize-celery.py

# celery worker -A app.worker -l info -Q main-queue -c 1
#celery worker -A app.worker -l INFO
#celery worker -A app.tasks.celery_app beat -l INFO

celery -A app.tasks.celery_app worker -l info
