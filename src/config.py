import json
import tomllib
import pathlib
from dataclasses import dataclass

from aiogram.types import BotCommand

__all__ = ('Config', 'load_config', 'BotCommand', 'load_commands')


@dataclass(frozen=True, slots=True)
class Config:
    country_code: str
    logfile_path: str
    bot_token: str
    api_url: str
    db_api_url: str
    auth_api_url: str
    debug: bool


def load_config(config_file_path: str | pathlib.Path) -> Config:
    with open(config_file_path, 'rb') as file:
        config = tomllib.load(file)
    return Config(
        country_code=config['app']['country_code'],
        logfile_path=config['app']['logfile_path'] or None,
        api_url=config['api']['dodo_api_url'],
        db_api_url=config['api']['database_api_url'],
        debug=config['app']['debug'],
        auth_api_url=config['api']['auth_api_url'],
        bot_token=config['app']['telegram_bot_token'],
    )


def load_commands(config_file_path: pathlib.Path) -> list[BotCommand]:
    if not config_file_path.exists():
        return []
    with open(config_file_path) as file:
        bot_commands = json.load(file)
    return [
        BotCommand(
            command=bot_command['command'],
            description=bot_command['description'],
        ) for bot_command in bot_commands
    ]
