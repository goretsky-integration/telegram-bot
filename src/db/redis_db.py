import redis.asyncio as redis

from config import app_settings
from utils import logger, exceptions

__all__ = (
    'get_cookies',
    'get_access_token',
    'close_redis_connection',
)

connection = redis.from_url(app_settings.redis_url, decode_responses=True)


@exceptions.raise_on_none(exceptions.NoCookiesError)
async def get_cookies(account_name: str) -> dict:
    return await connection.hgetall(account_name)


@exceptions.raise_on_none(exceptions.NoTokenError)
async def get_access_token(account_name: str) -> str:
    return await connection.hget('tokens', account_name)


async def close_redis_connection():
    await connection.close()
    logger.debug('Redis connection has been closed')
