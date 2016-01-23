#!/bin/bash
FILENAME=$(date +"%Y-%m-%d")

PYTHONPATH=`pwd`:/d/sergiysavarin.fortytwotesttask1-4/uwsgi DJANGO_SETTINGS_MODULE=fortytwo_test_task.settings django-admin.py models_count 2> $FILENAME.dat 1> /dev/null
