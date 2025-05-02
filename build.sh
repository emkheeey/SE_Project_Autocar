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
mkdir -p AutoCar/staticfiles_build

# Run collectstatic to gather all static files
echo "Collecting static files..."
cd AutoCar
python3 manage.py collectstatic --noinput --clear

# Create a special directory structure for Vercel
echo "Setting up Vercel static directory structure..."
mkdir -p staticfiles_build/static
cp -r staticfiles/* staticfiles_build/static/

# Create test files to verify static serving
echo "Creating test files..."
echo "This is a test file to verify static serving" > staticfiles_build/static/test.txt

# Create a touch file in each directory to ensure they exist
touch staticfiles_build/static/css/.keep
touch staticfiles_build/static/js/.keep
touch staticfiles_build/static/images/.keep

# Debug - list static files
echo "Static files collected. Contents of staticfiles_build directory:"
ls -la staticfiles_build/static
ls -la staticfiles_build/static/css || echo "css directory missing or empty"
ls -la staticfiles_build/static/js || echo "js directory missing or empty"
ls -la staticfiles_build/static/images || echo "images directory missing or empty"

# Return to root directory
cd ..

echo "Build process completed successfully!" 