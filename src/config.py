import tomllib
import pathlib
from dataclasses import dataclass

from pydantic import BaseSettings, Field

__all__ = (
    'ROOT_PATH',
    'LOG_FILE_PATH',
)

ROOT_PATH = pathlib.Path(__file__).parent.parent
LOG_FILE_PATH = ROOT_PATH / 'logs.log'


@dataclass(frozen=True, slots=True)
class Config:
    bot_token: str
    api_url: str
    db_api_url: str
    debug: bool


class AppSettings(BaseSettings):
    bot_token: str = Field(..., env='TELEGRAM_BOT_TOKEN')
    api_url: str = Field(..., env='DODO_API_URL')
    db_api_url: str = Field(..., env='DB_API_URL')
    debug: bool = Field(..., env='DEBUG')


def load_config(config_file_path: str | pathlib.Path) -> Config:
    with open(config_file_path, 'rb') as file:
        config = tomllib.load(file)
    return Config(
        api_url=config['api']['dodo_api_url'],
        db_api_url=config['api']['database_api_url'],
        debug=config['app']['debug'],
        bot_token=config['app']['telegram_bot_token'],
    )
