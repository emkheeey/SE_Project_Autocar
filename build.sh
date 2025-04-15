#!/bin/bash

# Install dependencies with upgrade to ensure we get the latest package versions
pip3 install --upgrade pip
pip3 install -r AutoCar/requirements.txt

# Verify Django is installed
python3 -c "import django; print(f'Django version: {django.__version__}')"

# Collect static files
cd AutoCar
python3 manage.py collectstatic --noinput 