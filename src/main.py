import functools
import logging
import pathlib

from aiogram import executor, Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from config import load_config, load_commands
from handlers import register_handlers
from middlewares import DependencyInjectMiddleware
from services.http_client_factory import closing_http_client_factory


async def setup_bot_commands(
        *,
        bot: Bot,
        commands_file_path: pathlib.Path,
) -> None:
    commands = load_commands(commands_file_path)
    await bot.set_my_commands(commands)


async def on_startup(dispatcher: Dispatcher):
    register_handlers(dispatcher)


def setup_logging(*, logfile_path: str | pathlib.Path, debug: bool) -> None:
    loglevel = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(filename=logfile_path, level=loglevel)


def main():
    root_path = pathlib.Path(__file__).parent.parent
    config_file_path = root_path / 'config.toml'
    commands_file_path = root_path / 'commands.json'

    config = load_config(config_file_path)

    setup_logging(logfile_path=config.logfile_path, debug=config.debug)

    bot = Bot(config.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot, storage=MemoryStorage())

    dp.setup_middleware(
        DependencyInjectMiddleware(
            country_code=config.country_code,
            auth_api_http_client_factory=functools.partial(
                closing_http_client_factory,
                base_url=config.auth_api_url,
            ),
            dodo_api_http_client_factory=functools.partial(
                closing_http_client_factory,
                base_url=config.api_url,
            ),
            database_api_http_client_factory=functools.partial(
                closing_http_client_factory,
                base_url=config.db_api_url,
            ),
        ),
    )

    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
    )


if __name__ == '__main__':
    main()
