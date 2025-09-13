import os
from django.core.asgi import get_asgi_application
import django

print(django.get_version())

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

import chat.routing
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack



print("DJANGO_SETTINGS_MODULE:", os.environ.get("DJANGO_SETTINGS_MODULE"))

application = ProtocolTypeRouter({
    "http": get_asgi_application(), 
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns
        )
        
    ), 
})
