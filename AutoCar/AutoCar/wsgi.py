"""
WSGI config for AutoCar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
import traceback

# Load environment variables from .env file if present
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("Loaded environment variables from .env file")
except Exception as e:
    print(f"Error loading .env file: {e}")

# Set up settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoCar.settings')

# Print diagnostics
print(f"Python version: {sys.version}")
print(f"PYTHONPATH: {sys.path}")
print(f"Current directory: {os.getcwd()}")
print(f"Settings module: {os.environ.get('DJANGO_SETTINGS_MODULE')}")

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("WSGI application initialized successfully")
except Exception as e:
    print(f"Error initializing WSGI application: {e}")
    print(traceback.format_exc())
    # Fallback to a simple error application
    def application(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        error_message = f"Server Error: Application initialization failed\n\n{traceback.format_exc()}"
        return [error_message.encode()]

# Vercel uses the variable 'app'
app = application
