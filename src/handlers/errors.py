import logging

from aiogram import Dispatcher
from aiogram.types import Update, InlineKeyboardMarkup, InlineKeyboardButton

from core import exceptions
from shortcuts import get_message


async def on_chat_is_not_found_error(update: Update,
                                     exception: exceptions.UserNotFoundError) -> bool:
    await get_message(update).answer(
        'Кажется, данный чат не зарегистрирован в моей системе 🙁',
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        '🚀 Зарегистрировать',
                        callback_data='register_current_chat',
                    )
                ]
            ]
        )
    )
    return True


async def on_application_error(update: Update,
                               exception: exceptions.ApplicationError) -> bool:
    message = update.message or update.callback_query.message
    match exception:
        case exceptions.NoEnabledUnitsError():
            await message.answer(
                'Кажется вы не добавили ни одну точку продаж для отображения 😕\n'
                'Чтобы это сделать, нажмите на кнопку ⚙️ Настройки или введите команду /settings.\n'
                'Далее нажмите на кнопку Отчёты по статистике и отметьте точки продаж.')
        case exceptions.DatabaseAPIServiceError():
            await message.answer('Произошла ошибка сервиса базы данных')
        case exceptions.DodoAPIServiceError():
            await message.answer('Произошла ошибка сервиса API')
        case exceptions.ApplicationError():
            logging.error(f'Application error: {str(exception)}')
            await message.answer('Произошла неизвестная ошибка')
    return True


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_errors_handler(
        on_chat_is_not_found_error,
        exception=exceptions.UserNotFoundError,
    )
    dispatcher.register_errors_handler(
        on_application_error,
        exception=exceptions.ApplicationError,
    )
