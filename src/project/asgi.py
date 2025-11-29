import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')

# Check if we're on Vercel (WebSocket not supported on free plan)
IS_VERCEL = os.environ.get('VERCEL_ENV') is not None

if IS_VERCEL:
    # On Vercel, only use HTTP (no WebSocket support)
    application = get_asgi_application()
else:
    # Local development with WebSocket support
    import django
    django.setup()
    
    import chat.routing
    from channels.routing import ProtocolTypeRouter, URLRouter
    from channels.auth import AuthMiddlewareStack
    
    application = ProtocolTypeRouter({
        "http": get_asgi_application(), 
        "websocket": AuthMiddlewareStack(
            URLRouter(
                chat.routing.websocket_urlpatterns
            )
        ), 
    })
