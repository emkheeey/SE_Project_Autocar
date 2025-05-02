#!/bin/bash
set -e

echo "Starting build process..."

# Print Python version for debugging
python3 --version

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Make sure staticfiles directory exists
echo "Making sure the staticfiles directory exists..."
mkdir -p AutoCar/staticfiles

# Run collectstatic to gather all static files
echo "Collecting static files..."
cd AutoCar
python3 manage.py collectstatic --noinput --clear

# Debugging: List static files
echo "Static files collected. Checking staticfiles directory:"
ls -la staticfiles
ls -la staticfiles/css
ls -la staticfiles/js
ls -la staticfiles/images

# Create a simple test file to verify static serving
echo "Creating test file..."
echo "This is a test file to verify static serving" > staticfiles/test.txt

# Return to root directory
cd ..

echo "Build process completed successfully!" 