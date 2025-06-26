from django.urls import re_path
from apps.task.consumers import NotificationConsumer

websocket_urlpatterns = [
    re_path(r"ws/notifications/$", NotificationConsumer.as_asgi()),
]
