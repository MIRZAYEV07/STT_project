from django.urls import path
from consumers.consumers_v1 import STTConsumer

websocket_urlpatterns = [
    path('ws/stt/', STTConsumer.as_asgi()),
]
