#!/bin/bash
set -e

echo "Starting build process..."

# Print Python version for debugging
python3 --version

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Debugging - list files to ensure correct directory structure
echo "Directory contents (before static collection):"
ls -la
ls -la AutoCar

# Make sure staticfiles directory exists
echo "Creating staticfiles directory if needed..."
mkdir -p AutoCar/staticfiles

# Run collectstatic to gather all static files
echo "Collecting static files..."
cd AutoCar
python3 manage.py collectstatic --noinput --clear

# Create a test file to verify static serving
echo "Creating test file..."
echo "This is a test file to verify static serving" > staticfiles/test.txt

# Debug - list static files
echo "Static files collected. Contents of staticfiles directory:"
ls -la staticfiles
ls -la staticfiles/css
ls -la staticfiles/js
ls -la staticfiles/images

# Return to root directory
cd ..

echo "Build process completed successfully!" 