#!/bin/bash
FILENAME=$(date +"%Y-%m-%d")

python manage.py models_count &> $FILENAME.dat
