"""
Vercel setup helper for static files and path configuration.
This is automatically imported by the wsgi.py file to ensure proper file paths on Vercel.
"""

import os
import sys
import logging

logger = logging.getLogger(__name__)

def setup_vercel_environment():
    """Configure the environment specifically for Vercel"""
    
    # Mark that we're running on Vercel
    os.environ['VERCEL'] = 'true'
    
    # Set static path configuration for Vercel environment
    current_dir = os.getcwd()
    logger.info(f"Current directory: {current_dir}")
    
    # Add current directory to path if not already there
    if current_dir not in sys.path:
        sys.path.insert(0, current_dir)
        logger.info(f"Added {current_dir} to path")
    
    # Log Python path
    logger.info(f"Python path: {sys.path}")
    
    # Check for staticfiles directory
    staticfiles_path = os.path.join(current_dir, 'AutoCar', 'staticfiles_build')
    if os.path.exists(staticfiles_path):
        logger.info(f"Found staticfiles_build at {staticfiles_path}")
    else:
        logger.warning(f"staticfiles_build directory not found at {staticfiles_path}")
        
    return True

# Run setup automatically when imported
setup_vercel_environment() 