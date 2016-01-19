#!/bin/bash
FILENAME=$(date +"%Y-%m-%d")

python manage.py models_count 2> $FILENAME.dat 1> /dev/null
