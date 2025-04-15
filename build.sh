#!/bin/bash
set -e

echo "Starting build process..."

# Print Python version for debugging
python3 --version

# Print directory contents for debugging
echo "Current directory: $(pwd)"
echo "Directory contents:"
ls -la

# Install dependencies
echo "Installing dependencies..."
pip3 install -r requirements.txt

# Print installed packages for debugging
echo "Installed packages:"
pip3 list

# Run migrations to create database tables
echo "Running database migrations..."
if [ -d "AutoCar" ]; then
  cd AutoCar
  python3 manage.py migrate
  python3 manage.py collectstatic --noinput
else
  # If running from root of AutoCar (Vercel's path0)
  python3 manage.py migrate
  python3 manage.py collectstatic --noinput
fi

# Verify Django is installed
echo "Verifying Django installation..."
python3 -c "import django; print(f'Django version: {django.__version__}')"

# Create required directories
echo "Ensuring staticfiles directory exists..."
mkdir -p AutoCar/staticfiles

echo "Build process completed successfully!" 