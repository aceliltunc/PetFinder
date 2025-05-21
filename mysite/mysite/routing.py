from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import mainpage.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            mainpage.routing.websocket_urlpatterns
        )
    ),
})

