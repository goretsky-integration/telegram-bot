from aiogram import executor, Bot, Dispatcher
from aiogram.types import ParseMode, BotCommand

import handlers
from config import get_app_settings
from middlewares import AuthClientMiddleware, DatabaseClientMiddleware, DodoAPIClientMiddleware


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
    handlers.start.register_handlers(dispatcher)
    handlers.settings.register_handlers(dispatcher)
    handlers.reports.register_handlers(dispatcher)


async def on_startup(dispatcher: Dispatcher):
    register_all_handlers(dispatcher)
    await setup_bot_commands(dispatcher.bot)


def main():
    app_settings = get_app_settings()
    bot = Bot(app_settings.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher(bot)

    dp.setup_middleware(AuthClientMiddleware(app_settings.db_api_url))
    dp.setup_middleware(DatabaseClientMiddleware(app_settings.db_api_url))
    dp.setup_middleware(DodoAPIClientMiddleware(app_settings.api_url))

    executor.start_polling(
        dispatcher=dp,
        skip_updates=True,
        on_startup=on_startup,
    )


if __name__ == '__main__':
    main()
