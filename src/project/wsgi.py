"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``handler`` for Vercel.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os
import sys

# Add src to Python path for Vercel
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

from django.core.wsgi import get_wsgi_application

# Initialize Django
django_app = get_wsgi_application()

# Vercel expects 'handler' variable - export WSGI application directly
handler = django_app
application = django_app
app = django_app
