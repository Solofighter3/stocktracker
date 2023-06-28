"""
ASGI config for stocktracker project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

import os
from mainapp.routing import websocket_urlpatterns
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter,URLRouter
from channels.auth import AuthMiddlewareStack
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stocktracker.settings')
#In order to handle websocket request we need to configure asgi settings so
#whenever websocket connection is initiated django will look for url routing in
#websocket_urlpatterns
application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket':AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns

            )               
        )
    })
