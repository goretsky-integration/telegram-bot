from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode, BotCommand

import db
from config import app_settings

__all__ = (
    'bot',
    'dp',
    'on_shutdown',
    'on_startup',
)

bot = Bot(app_settings.bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


async def setup_bot_commands(bot: Bot):
    await bot.set_my_commands([
        BotCommand('start', '👨‍💻 Главное меню'),
        BotCommand('settings', '⚙️ Настройки'),
        BotCommand('reports', '🔎 Отчёты по статистике'),
        BotCommand('bonus_system', 'Бонусная система'),
        BotCommand('cooking_time', 'Время приготовления'),
        BotCommand('restaurant_cooking_time', 'Время приготовления (ресторан)'),
        BotCommand('daily_revenue', 'Выручка за сегодня'),
        BotCommand('delivery_speed', 'Скорость доставки'),
        BotCommand('delivery_awaiting_time', 'Время на полке'),
        BotCommand('kitchen_performance', 'Производительность кухни'),
        BotCommand('delivery_performance', 'Производительность доставки'),
        BotCommand('being_late_certificates', 'Сертификаты за опоздание'),
        BotCommand('awaiting_orders', 'Заказов остывает на полке - курьеры всего / в очереди'),

    ])


async def on_startup(dispatcher: Dispatcher):
    await setup_bot_commands(dispatcher.bot)


async def on_shutdown(dispatcher: Dispatcher):
    await db.close_redis_connection()
