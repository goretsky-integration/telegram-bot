from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from dodolib import DodoAPIClient

__all__ = ('DodoAPIClientMiddleware',)


class DodoAPIClientMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, base_url: str):
        super().__init__()
        self.__base_url = base_url

    async def pre_process(self, obj, data: dict, *args):
        data['api_client'] = DodoAPIClient(self.__base_url)

    async def post_process(self, obj, data: dict, *args):
        api_client: DodoAPIClient = data['api_client']
        await api_client.close()
