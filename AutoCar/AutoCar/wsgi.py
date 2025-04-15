"""
WSGI config for AutoCar project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys
import traceback
import json

# Import path setup script for Vercel
try:
    # Import the Vercel-specific setup script
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    import vercel_setup
    print("Imported vercel_setup script")
except Exception as e:
    print(f"Error importing vercel_setup: {e}")

# Additional diagnostics at module level
print(f"Initial directory listing: {os.listdir()}")

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

# Define a health check application
def health_check_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'application/json')]
    start_response(status, response_headers)
    
    # Collect diagnostic info
    env_copy = dict(os.environ)
    # Remove sensitive info
    for key in ['SECRET_KEY', 'DATABASE_URL', 'SUPABASE_KEY']:
        if key in env_copy:
            env_copy[key] = '[REDACTED]'
    
    info = {
        'status': 'healthy',
        'python_version': sys.version,
        'current_dir': os.getcwd(),
        'dir_contents': os.listdir(),
        'sys_path': sys.path,
        'environment': env_copy
    }
    
    return [json.dumps(info, default=str).encode()]

try:
    from django.core.wsgi import get_wsgi_application
    application = get_wsgi_application()
    print("WSGI application initialized successfully")
except Exception as e:
    print(f"Error initializing WSGI application: {e}")
    print(traceback.format_exc())
    # Fallback to a simple error application
    def application(environ, start_response):
        path_info = environ.get('PATH_INFO', '')
        
        # Handle diagnostic endpoint
        if path_info == '/health/' or path_info == '/health':
            return health_check_app(environ, start_response)
        
        # Default error handler for other paths
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/html')]
        start_response(status, response_headers)
        
        error_html = f"""
        <html>
        <head><title>Application Error</title></head>
        <body>
            <h1>Server Error: Application initialization failed</h1>
            <p>{str(e)}</p>
            <pre>{traceback.format_exc()}</pre>
            <h2>Diagnostics:</h2>
            <p>Python version: {sys.version}</p>
            <p>Current directory: {os.getcwd()}</p>
            <p>Directory contents: {os.listdir()}</p>
            <p>PYTHONPATH: {sys.path}</p>
            <p><a href="/health/">View detailed diagnostics</a></p>
        </body>
        </html>
        """
        return [error_html.encode()]

# Vercel uses the variable 'app'
app = application
