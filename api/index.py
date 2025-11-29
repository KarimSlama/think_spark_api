import os
import sys

# Add src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Get Django WSGI application
from django.core.wsgi import get_wsgi_application

# Vercel expects 'app' variable
app = get_wsgi_application()

