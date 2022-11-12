from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from dodolib import DatabaseClient

__all__ = ('DatabaseClientMiddleware',)


class DatabaseClientMiddleware(LifetimeControllerMiddleware):
    skip_patterns = ['error', 'update']

    def __init__(self, base_url: str):
        super().__init__()
        self.__base_url = base_url

    async def pre_process(self, obj, data: dict, *args):
        data['db_client'] = DatabaseClient(self.__base_url)

    async def post_process(self, obj, data: dict, *args):
        db_client: DatabaseClient = data['db_client']
        await db_client.close()
