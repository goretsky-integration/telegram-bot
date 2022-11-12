from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from dodolib import AuthClient

__all__ = ('AuthClientMiddleware',)


class AuthClientMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, base_url: str):
        super().__init__()
        self.__base_url = base_url

    async def pre_process(self, obj, data: dict, *args):
        data['auth_client'] = AuthClient(self.__base_url)

    async def post_process(self, obj, data: dict, *args):
        auth_client: AuthClient = data['auth_client']
        await auth_client.close()
