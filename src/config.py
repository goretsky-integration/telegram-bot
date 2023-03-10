import tomllib
import pathlib
from dataclasses import dataclass

__all__ = ('Config', 'load_config')


@dataclass(frozen=True, slots=True)
class Config:
    logfile_path: str
    bot_token: str
    api_url: str
    db_api_url: str
    debug: bool


def load_config(config_file_path: str | pathlib.Path) -> Config:
    with open(config_file_path, 'rb') as file:
        config = tomllib.load(file)
    return Config(
        logfile_path=config['app']['logfile_path'] or None,
        api_url=config['api']['dodo_api_url'],
        db_api_url=config['api']['database_api_url'],
        debug=config['app']['debug'],
        bot_token=config['app']['telegram_bot_token'],
    )
