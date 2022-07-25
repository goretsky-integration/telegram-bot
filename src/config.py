from dotenv import load_dotenv
from pydantic import BaseSettings, Field

__all__ = (
    'app_settings',
)

load_dotenv()


class AppSettings(BaseSettings):
    bot_token: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    api_url: str = Field(..., env='DODO_API_URL')
    db_api_url: str = Field(..., env='DB_API_URL')
    mongo_db_url: str = Field(..., env='MONGO_DB_URL')
    redis_url: str = Field(..., env='REDIS_URL')
    debug: bool = Field(..., env='DEBUG')


app_settings = AppSettings()
