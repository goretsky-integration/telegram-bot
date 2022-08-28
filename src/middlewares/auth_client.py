from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from dodolib import AuthClient

from services.dependencies import get_auth_client

__all__ = (
    'AuthClientMiddleware',
)


class AuthClientMiddleware(LifetimeControllerMiddleware):

    async def pre_process(self, obj, data: dict, *args):
        data['auth_client'] = get_auth_client()

    async def post_process(self, obj, data: dict, *args):
        auth_client: AuthClient = data['auth_client']
        await auth_client.close()
