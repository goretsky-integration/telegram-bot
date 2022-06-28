from motor.motor_asyncio import AsyncIOMotorClient
from config import app_settings

__all__ = (
    'client',
    'database',
)

client = AsyncIOMotorClient(app_settings.mongo_db_url)
database = client.dodo
