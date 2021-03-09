#!/bin/bash
python manage.py makemigrations
python manage.py migrate
gunicorn application.asgi:application -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000