from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/data/$', consumers.DataConsumer.as_asgi()),
    re_path(r'ws/time/$', consumers.TimeConsumer.as_asgi()),
    re_path(r'ws/weather/$', consumers.WeatherConsumer.as_asgi()),
]