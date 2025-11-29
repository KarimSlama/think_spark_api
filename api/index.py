import os
import sys

# Add src directory to Python path
src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if src_path not in sys.path:
    sys.path.insert(0, src_path)

# Set Django settings module before any Django imports
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Import and create WSGI application
from django.core.wsgi import get_wsgi_application

# Vercel expects 'app' variable
app = get_wsgi_application()

