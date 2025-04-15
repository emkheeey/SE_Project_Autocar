from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
import os
import sys

def test_view(request):
    """
    Simple view to test if the application is working
    """
    html = f"""
    <html>
    <head><title>Django Test</title></head>
    <body>
        <h1>Django is running!</h1>
        <p>Python version: {sys.version}</p>
        <p>Debug mode: {os.environ.get('DEBUG', 'Not set')}</p>
        <p>Current directory: {os.getcwd()}</p>
        <pre>Environment Variables:
        {', '.join(f"{k}" for k in os.environ.keys())}
        </pre>
    </body>
    </html>
    """
    return HttpResponse(html)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),  # Include the accounts app URLs
    path('test/', test_view, name='test_view'),  # Add a test view
]