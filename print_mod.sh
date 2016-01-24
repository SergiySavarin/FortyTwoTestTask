#!/bin/bash
FILENAME=$(date +"%Y-%m-%d")

pwd
PYTHONPATH=`pwd`:/d/sergiysavarin.fortytwotesttask1-4/uwsgi DJANGO_SETTINGS_MODULE=settings_deploy django-admin.py models_count 2> $FILENAME.dat 1> /dev/null
