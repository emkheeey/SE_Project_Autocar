#!/bin/bash
set -e

echo "Starting build process..."

# Install dependencies with upgrade to ensure we get the latest package versions
echo "Upgrading pip and installing dependencies..."
pip3 install --upgrade pip
pip3 install -r AutoCar/requirements.txt

# Verify Django is installed
echo "Verifying Django installation..."
python3 -c "import django; print(f'Django version: {django.__version__}')"

# Create required directories
echo "Ensuring staticfiles directory exists..."
mkdir -p AutoCar/staticfiles

# Collect static files
echo "Collecting static files..."
cd AutoCar
python3 manage.py collectstatic --noinput --verbosity 1

echo "Build process completed successfully!" 