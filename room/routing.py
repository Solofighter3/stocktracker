from django.urls import path
from . import consumers

websocket_urlpatternns=[
                path(r'ws/<str:room_name>/',consumers.Chatconsumer.as_asgi())
        ]
