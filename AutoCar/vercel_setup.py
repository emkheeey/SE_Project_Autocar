"""
Vercel setup script to fix import paths.
This should be imported at the top of the wsgi.py file.
"""

import os
import sys
import importlib.util

def setup_paths():
    """Set up Python path for Vercel deployment"""
    
    # Get the current directory
    current_dir = os.getcwd()
    print(f"Current directory: {current_dir}")
    
    # Add current directory to path if not already there
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        print(f"Added {current_dir} to path")
    
    # If we're in /var/task (Vercel), add the AutoCar directory to path
    if current_dir == '/var/task':
        autocar_path = os.path.join(current_dir, 'AutoCar')
        if os.path.exists(autocar_path) and autocar_path not in sys.path:
            sys.path.insert(0, autocar_path)
            print(f"Added {autocar_path} to path")
    
    # Check if supabase_utils exists and ensure it's importable
    if os.path.exists('supabase_utils.py'):
        print("supabase_utils.py found in current directory")
    else:
        print("supabase_utils.py not found in current directory")
        
    # Print the final Python path
    print(f"Final Python path: {sys.path}")

# Run setup when module is imported
setup_paths() 