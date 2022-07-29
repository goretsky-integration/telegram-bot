from aiogram.types import Update

from bot import dp
from utils import exceptions


@dp.errors_handler(exception=exceptions.NoTokenError)
@dp.errors_handler(exception=exceptions.NoCookiesError)
async def on_no_token_or_cookies_error(update: Update, exception: exceptions.NoTokenError | exceptions.NoCookiesError):
    if update.callback_query is not None:
        await update.callback_query.answer('Ошибка авторизации', show_alert=True)
    elif update.message is not None:
        await update.message.answer('Ошибка авторизации')
    return True


@dp.errors_handler(exception=exceptions.DodoAPIError)
async def on_dodo_api_error(update: Update, exception: exceptions.DodoAPIError):
    if update.callback_query is not None:
        await update.callback_query.answer('Произошла ошибка', show_alert=True)
    elif update.message is not None:
        await update.message.answer('Произошла ошибка')
    return True
