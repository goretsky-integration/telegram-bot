from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode

from config import app_settings

__all__ = (
    'bot',
    'dp',
)

bot = Bot(app_settings.bot_token, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)
