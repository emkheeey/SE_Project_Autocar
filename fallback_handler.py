"""
Fallback handler for Vercel that doesn't depend on Django.
This can be used to diagnose issues with the environment.
"""

import os
import sys
import json
import traceback

def get_environment_info():
    """Get information about the environment"""
    # Get Python version and path
    python_info = {
        'version': sys.version,
        'executable': sys.executable,
        'path': sys.path
    }
    
    # Get environment variables (hiding sensitive ones)
    env_vars = {}
    for key, value in os.environ.items():
        if key in ['SECRET_KEY', 'DATABASE_URL', 'SUPABASE_KEY']:
            env_vars[key] = '[REDACTED]'
        else:
            env_vars[key] = value
            
    # Get directory contents
    try:
        dir_contents = os.listdir()
    except Exception as e:
        dir_contents = f"Error listing directory: {str(e)}"
    
    # Try to import key modules
    import_tests = {}
    modules_to_test = [
        'django', 
        'django.conf', 
        'django.http', 
        'supabase',
        'dotenv',
        'asgiref',
        'sqlparse'
    ]
    
    for module in modules_to_test:
        try:
            __import__(module)
            import_tests[module] = 'Successfully imported'
        except ImportError as e:
            import_tests[module] = f'Import error: {str(e)}'
        except Exception as e:
            import_tests[module] = f'Error: {str(e)}'
    
    # Return all info as a dictionary
    return {
        'python': python_info,
        'environment': env_vars,
        'directory_contents': dir_contents,
        'import_tests': import_tests,
        'current_directory': os.getcwd()
    }

def application(environ, start_response):
    """WSGI application for fallback handler"""
    # Always return 200 OK with JSON response
    start_response('200 OK', [('Content-Type', 'application/json')])
    
    try:
        # Get environment info
        info = get_environment_info()
        
        # Get request info
        request_info = {
            'path': environ.get('PATH_INFO', ''),
            'method': environ.get('REQUEST_METHOD', ''),
            'query_string': environ.get('QUERY_STRING', ''),
            'server_name': environ.get('SERVER_NAME', ''),
            'server_port': environ.get('SERVER_PORT', '')
        }
        
        # Combine all info
        response_data = {
            'status': 'Fallback handler active',
            'message': 'This is the fallback handler, Django application failed to load',
            'request': request_info,
            'environment': info
        }
        
        # Return JSON response
        return [json.dumps(response_data, default=str).encode('utf-8')]
    except Exception as e:
        # If anything goes wrong, return error info
        error_data = {
            'status': 'error',
            'message': f'Error in fallback handler: {str(e)}',
            'traceback': traceback.format_exc()
        }
        return [json.dumps(error_data, default=str).encode('utf-8')]

# Make it compatible with Vercel
app = application 