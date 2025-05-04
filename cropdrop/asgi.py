import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import cropdrop.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "cropdrop.settings")

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AuthMiddlewareStack(
            URLRouter(cropdrop.routing.websocket_urlpatterns)
        ),
    }
)
