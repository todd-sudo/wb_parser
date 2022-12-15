#!/bin/bash
docker-compose -f stage.yml up --build -d --scale celeryworker=5
