import functools
import logging
import pathlib

from aiogram import executor, Bot, Dispatcher
from aiogram.types import ParseMode, BotCommand

import handlers
from config import load_config
from middlewares import DependencyInjectMiddleware
from services.database_api import DatabaseAPIService
from services.dodo_api import DodoAPIService
from services.auth_api import AuthAPIService
from services.http_client_factory import closing_http_client_factory


async def setup_bot_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand('bonus_system', 'Бонусная система'),
        BotCommand('cooking_time', 'Время приготовления (общее)'),
        BotCommand('restaurant_cooking_time', 'Время приготовления (ресторан)'),
        BotCommand('daily_revenue', 'Выручка за сегодня'),
        BotCommand('delivery_speed', 'Скорость доставки'),
        BotCommand('delivery_awaiting_time', 'Время на полке'),
        BotCommand('kitchen_performance', 'Производительность кухни'),
        BotCommand('delivery_performance', 'Производительность доставки'),
        BotCommand('being_late_certificates', 'Сертификаты за опоздание'),
        BotCommand('awaiting_orders', 'Заказов остывает на полке - курьеры всего / в очереди'),
        BotCommand('productivity_balance', 'Баланс эффективности'),
        BotCommand('start', '👨‍💻 Главное меню'),
        BotCommand('settings', '⚙️ Настройки'),
        BotCommand('reports', '🔎 Отчёты по статистике'),
        BotCommand('show_keyboard', 'Показать клавиатуру'),
        BotCommand('hide_keyboard', 'Скрыть клавиатуру'),
    ])


def register_all_handlers(dispatcher: Dispatcher):
    handlers.errors.register_handlers(dispatcher)
    handlers.start.register_handlers(dispatcher)
    handlers.settings.register_handlers(dispatcher)
    handlers.reports.register_handlers(dispatcher)


async def on_startup(dispatcher: Dispatcher):
    register_all_handlers(dispatcher)
    await setup_bot_commands(dispatcher.bot)


def setup_logging(*, logfile_path: str | pathlib.Path, debug: bool) -> None:
    loglevel = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(filename=logfile_path, level=loglevel)


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.toml'
    config = load_config(config_file_path)

    setup_logging(logfile_path=config.logfile_path, debug=config.debug)

    bot = Bot(config.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot)

    database_api_service = DatabaseAPIService(
        http_client_factory=functools.partial(
            closing_http_client_factory,
            base_url=config.db_api_url,
        ),
    )
    dodo_api_service = DodoAPIService(
        http_client_factory=functools.partial(
            closing_http_client_factory,
            base_url=config.api_url,
        ),
        country_code='ru',
    )
    auth_api_service = AuthAPIService(
        http_client_factory=functools.partial(
            closing_http_client_factory,
            base_url=config.db_api_url,
        )
    )
    dp.setup_middleware(
        DependencyInjectMiddleware(
            dodo_api_service=dodo_api_service,
            database_api_service=database_api_service,
            auth_api_service=auth_api_service,
        ),
    )

    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
    )


if __name__ == '__main__':
    main()
