#!/bin/bash

# Install dependencies
pip3 install -r AutoCar/requirements.txt

# Run migrations
cd AutoCar
python3 manage.py collectstatic --noinput