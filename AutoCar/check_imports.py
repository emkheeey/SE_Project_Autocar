#!/usr/bin/env python
"""
Test script to verify imports and settings in the Django project.
"""

import os
import sys
import importlib

print(f"Current working directory: {os.getcwd()}")
print(f"Python path: {sys.path}")
print(f"Directory contents: {os.listdir()}")

# Add the project root to path
if '.' not in sys.path:
    sys.path.append('.')
    print("Added current directory to path")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AutoCar.settings')

print("\nTrying to import Django modules...")
try:
    import django
    print(f"Django version: {django.__version__}")
    
    print("\nTrying to import settings...")
    try:
        from django.conf import settings
        print("Successfully imported settings")
        print(f"INSTALLED_APPS: {settings.INSTALLED_APPS}")
        print(f"ROOT_URLCONF: {settings.ROOT_URLCONF}")
        print(f"DATABASES: {settings.DATABASES.keys()}")
    except Exception as e:
        print(f"Error importing settings: {e}")
    
    print("\nTrying to import URLs...")
    try:
        importlib.import_module('AutoCar.urls')
        print("Successfully imported URLs")
    except Exception as e:
        print(f"Error importing URLs: {e}")
    
    print("\nTrying to import accounts app...")
    try:
        importlib.import_module('accounts.urls')
        print("Successfully imported accounts URLs")
    except Exception as e:
        print(f"Error importing accounts URLs: {e}")
    
    print("\nTrying to import supabase utils...")
    try:
        import supabase_utils
        print("Successfully imported supabase_utils")
    except Exception as e:
        print(f"Error importing supabase_utils: {e}")
    
except Exception as e:
    print(f"Error importing Django: {e}")

print("\nImport test completed") 