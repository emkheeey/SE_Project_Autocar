#!/bin/bash

# Install dependencies
pip install -r AutoCar/requirements.txt

# Make directory if it doesn't exist
mkdir -p staticfiles_build

# Collect static files
python AutoCar/manage.py collectstatic --noinput