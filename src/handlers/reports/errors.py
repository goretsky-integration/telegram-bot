from aiogram import Dispatcher
from aiogram.types import Update

from shortcuts import get_message
from utils import exceptions

__all__ = ('register_handlers',)


async def on_dodo_api_error(update: Update, exception):
    text = 'Произошла ошибка сервиса Dodo API 😔\nПопробуйте ещё раз'
    if update.message is not None:
        await update.message.reply(text)
    elif update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    return True


async def on_auth_api_error(update: Update, exception):
    text = 'Произошла ошибка сервиса авторизации 😔\nПопробуйте ещё раз'
    if update.message is not None:
        await update.message.reply(text)
    elif update.callback_query is not None:
        await update.callback_query.answer(text, show_alert=True)
    return True


async def on_no_enabled_units_error(update: Update, exception):
    await get_message(update).answer(
        'Кажется вы не добавили ни одну точку продаж для отображения 😕\n'
        'Чтобы это сделать, нажмите на кнопку ⚙️ Настройки или введите команду /settings.\n'
        'Далее нажмите на кнопку Отчёты по статистике и отметьте точки продаж.')
    return True


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_errors_handler(
        on_dodo_api_error,
        exception=exceptions.DodoAPIError,
    )
    dispatcher.register_errors_handler(
        on_auth_api_error,
        exception=exceptions.AuthAPIError,
    )
    dispatcher.register_errors_handler(
        on_no_enabled_units_error,
        exception=exceptions.NoEnabledUnitsError,
    )
