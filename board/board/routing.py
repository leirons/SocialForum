from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import mysite.routing as chat

application = ProtocolTypeRouter({
    "websocket":AuthMiddlewareStack(
        URLRouter(chat.websocket_urlpatterns)
    )
})