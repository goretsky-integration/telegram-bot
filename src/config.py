import pathlib
from functools import lru_cache

from dotenv import load_dotenv
from pydantic import BaseSettings, Field

__all__ = (
    'ROOT_PATH',
    'LOG_FILE_PATH',
    'get_app_settings',
)

ROOT_PATH = pathlib.Path(__file__).parent.parent
LOG_FILE_PATH = ROOT_PATH / 'logs.log'


class AppSettings(BaseSettings):
    bot_token: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    api_url: str = Field(..., env='DODO_API_URL')
    db_api_url: str = Field(..., env='DB_API_URL')
    debug: bool = Field(..., env='DEBUG')


@lru_cache
def get_app_settings() -> AppSettings:
    load_dotenv()
    return AppSettings()
