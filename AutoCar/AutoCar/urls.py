from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import os
import sys
import traceback
from django.conf import settings

def test_view(request):
    """
    Simple view to test if the application is working
    """
    try:
        # Gather system info
        python_version = sys.version
        debug_mode = settings.DEBUG
        current_dir = os.getcwd()
        env_vars = ', '.join(f"{k}" for k in os.environ.keys())
        
        # Test database connection
        db_info = "Not configured"
        try:
            from django.db import connections
            from django.db.utils import OperationalError
            conn = connections['default']
            try:
                conn.cursor()
                db_info = f"Connected to {settings.DATABASES['default']['ENGINE']}"
            except OperationalError:
                db_info = "Database connection failed"
        except Exception as e:
            db_info = f"Error checking database: {str(e)}"
        
        # Test Supabase connection
        supabase_info = "Not configured"
        try:
            from supabase_utils import get_supabase_client
            client = get_supabase_client()
            if client:
                supabase_info = "Supabase client created successfully"
            else:
                supabase_info = "Supabase client not created (URL or key missing)"
        except Exception as e:
            supabase_info = f"Error with Supabase: {str(e)}"
            
        html = f"""
        <html>
        <head>
            <title>Django Test</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                h1 {{ color: green; }}
                .section {{ margin-bottom: 20px; border: 1px solid #ddd; padding: 10px; }}
                pre {{ background-color: #f5f5f5; padding: 10px; white-space: pre-wrap; }}
            </style>
        </head>
        <body>
            <h1>Django is running!</h1>
            
            <div class="section">
                <h2>System Info</h2>
                <p><strong>Python version:</strong> {python_version}</p>
                <p><strong>Debug mode:</strong> {debug_mode}</p>
                <p><strong>Current directory:</strong> {current_dir}</p>
            </div>
            
            <div class="section">
                <h2>Database</h2>
                <p>{db_info}</p>
            </div>
            
            <div class="section">
                <h2>Supabase</h2>
                <p>{supabase_info}</p>
            </div>
            
            <div class="section">
                <h2>Environment Variables</h2>
                <pre>{env_vars}</pre>
            </div>
            
            <div class="section">
                <h2>Navigation</h2>
                <p><a href="/">Go to Home Page</a></p>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)
    except Exception as e:
        error_html = f"""
        <html>
        <head><title>Error in Test View</title></head>
        <body>
            <h1>Error in Test View</h1>
            <p>{str(e)}</p>
            <pre>{traceback.format_exc()}</pre>
        </body>
        </html>
        """
        return HttpResponse(error_html, status=500)

def error_view(request):
    """
    Simple view that always succeeds, for troubleshooting
    """
    return HttpResponse("Server is running. Basic functionality OK.")

def health_check(request):
    """
    Extremely simple health check endpoint
    """
    return HttpResponse("OK", content_type="text/plain")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Include the accounts app URLs
    path('test/', test_view, name='test_view'),  # Add a test view
    path('error-check/', error_view, name='error_view'),  # Always succeeds
    path('health/', health_check, name='health_check'),  # Simple health check
]