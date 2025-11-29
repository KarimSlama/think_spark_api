# Vercel serverless function entry point
import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Import Django WSGI application
from django.core.wsgi import get_wsgi_application

# Vercel Python runtime expects 'app' variable (not 'handler')
app = get_wsgi_application()

# Also export as 'handler' and 'application' for compatibility
handler = app
application = app

