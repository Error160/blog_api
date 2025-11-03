# +++++++++++ DJANGO +++++++++++
# To use your own Django app use code like this:
import os
import sys

# Add your project directory to the sys.path
path = '/home/YOUR_USERNAME/dummy_api'  # ⚠️ CHANGE THIS to your PythonAnywhere path
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables
os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

# Activate your virtual environment
# IMPORTANT: Update the path below to match your virtualenv path on PythonAnywhere
virtualenv_path = '/home/YOUR_USERNAME/dummy_api/venv'  # ⚠️ CHANGE THIS
activate_this = os.path.join(virtualenv_path, 'bin/activate_this.py')

# For Python 3.x, use exec with open
if os.path.exists(activate_this):
    with open(activate_this) as f:
        exec(f.read(), {'__file__': activate_this})

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

