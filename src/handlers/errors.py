import logging

from aiogram import Dispatcher
from aiogram.types import Update

from core import exceptions


async def on_database_api_service_error(update: Update, exception: exceptions.DatabaseAPIServiceError) -> bool:
    message = update.message or update.callback_query.message
    logging.error(f'Application error: {str(exception)}')
    await message.answer('Произошла ошибка сервиса базы данных')
    return True


async def on_application_error(update: Update, exception: exceptions.ApplicationError) -> bool:
    message = update.message or update.callback_query.message
    logging.error(f'Application error: {str(exception)}')
    await message.answer('Произошла неизвестная ошибка')
    return True


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_errors_handler(
        on_database_api_service_error,
        exception=exceptions.DatabaseAPIServiceError,
    )
    dispatcher.register_errors_handler(
        on_application_error,
        exception=exceptions.ApplicationError,
    )
