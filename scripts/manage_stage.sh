#!/bin/bash
docker-compose -f stage.yml run --rm django ./manage.py $@
