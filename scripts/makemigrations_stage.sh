#!/bin/bash
docker-compose -f stage.yml run --rm django python manage.py makemigrations
