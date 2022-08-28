from aiogram.dispatcher.middlewares import LifetimeControllerMiddleware
from dodolib import DatabaseClient

from services.dependencies import get_db_client

__all__ = (
    'DBAPIClientMiddleware',
)


class DBAPIClientMiddleware(LifetimeControllerMiddleware):

    async def pre_process(self, obj, data: dict, *args):
        data['db'] = get_db_client()

    async def post_process(self, obj, data: dict, *args):
        db: DatabaseClient = data['db']
        await db.close()
