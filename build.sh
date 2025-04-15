#!/bin/bash

# Install dependencies
pip3 install -r AutoCar/requirements.txt

# Collect static files
cd AutoCar
python3 manage.py collectstatic --noinput 