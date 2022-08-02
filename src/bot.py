from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode, BotCommand

from config import app_settings
from middlewares import DBAPIClientMiddleware, AuthClientMiddleware, DodoAPIClientMiddleware

__all__ = (
    'bot',
    'dp',
    'on_startup',
)

bot = Bot(app_settings.bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


def setup_middlewares(dispatcher: Dispatcher):
    dispatcher.setup_middleware(DBAPIClientMiddleware())
    dispatcher.setup_middleware(AuthClientMiddleware())
    dispatcher.setup_middleware(DodoAPIClientMiddleware())


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
        BotCommand('start', '👨‍💻 Главное меню'),
        BotCommand('settings', '⚙️ Настройки'),
        BotCommand('reports', '🔎 Отчёты по статистике'),
        BotCommand('show_keyboard', 'Показать клавиатуру'),
        BotCommand('hide_keyboard', 'Скрыть клавиатуру'),
    ])


async def on_startup(dispatcher: Dispatcher):
    setup_middlewares(dispatcher)
    await setup_bot_commands(dispatcher.bot)
