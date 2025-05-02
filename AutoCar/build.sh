#!/bin/bash
set -e

echo "Starting build process..."

# Install dependencies
pip3 install -r requirements.txt

# Make sure staticfiles directory exists
mkdir -p staticfiles

# Run collectstatic
echo "Collecting static files..."
python3 manage.py collectstatic --noinput

# Print static files info
echo "Static files collected. Contents of staticfiles directory:"
ls -la staticfiles

echo "Build process completed successfully!"