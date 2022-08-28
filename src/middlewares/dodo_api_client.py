from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from dodolib import DodoAPIClient

from services.dependencies import get_dodo_api_client

__all__ = (
    'DodoAPIClientMiddleware',
)


class DodoAPIClientMiddleware(LifetimeControllerMiddleware):

    async def pre_process(self, obj, data: dict, *args):
        data['dodo_client'] = get_dodo_api_client()

    async def post_process(self, obj, data: dict, *args):
        dodo_api_client: DodoAPIClient = data['dodo_client']
        await dodo_api_client.close()
