from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

import db
from config import app_settings

__all__ = (
    'bot',
    'dp',
    'on_shutdown',
)

bot = Bot(app_settings.bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)


async def on_shutdown(dispatcher: Dispatcher):
    await db.close_redis_connection()
