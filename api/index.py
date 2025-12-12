"""
Vercel serverless function handler for Django
Vercel's Python runtime expects a WSGI application exported as 'app'
"""
import os
import sys

# Add the project root to the Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.insert(0, project_root)

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Export WSGI application as 'app' for Vercel Python runtime
# Vercel automatically handles WSGI applications when exported as 'app'
app = get_wsgi_application()
