#!/bin/bash
set -e

echo "Starting build process..."

# Print Python version for debugging
python3 --version

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Make sure staticfiles directory exists
echo "Creating staticfiles directory if needed..."
mkdir -p AutoCar/staticfiles

# Run collectstatic to gather all static files
echo "Collecting static files..."
cd AutoCar
python3 manage.py collectstatic --noinput --clear

# Create test files to verify static serving
echo "Creating test files..."
echo "This is a test file to verify static serving" > staticfiles/test.txt

# Create a touch file in each directory to ensure they exist
touch staticfiles/css/.keep
touch staticfiles/js/.keep
touch staticfiles/images/.keep

# Debug - list static files
echo "Static files collected. Contents of staticfiles directory:"
ls -la staticfiles
ls -la staticfiles/css || echo "css directory missing or empty"
ls -la staticfiles/js || echo "js directory missing or empty"
ls -la staticfiles/images || echo "images directory missing or empty"

# Return to root directory
cd ..

echo "Build process completed successfully!" 