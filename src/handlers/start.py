import contextlib
import logging

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, ChatType

from core import exceptions
from services.database_api import DatabaseAPIService
from services.http_client_factory import HTTPClientFactory
from services.mappers import map_chat_to_create_dto, map_user_to_create_dto
from shortcuts import answer_views
from views import SettingsMenuView, StatisticsReportsMenuView, ShowKeyboardView

__all__ = ('register_handlers',)

logger = logging.getLogger('telegram_bot')


async def register_current_private_chat(
        callback_query: CallbackQuery,
        database_api_http_client_factory: HTTPClientFactory,
):
    logger.debug('Register private chat %d', callback_query.message.chat.id)

    user_to_create = map_user_to_create_dto(callback_query.from_user)

    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)

        try:
            await database_api_service.create_chat(user_to_create)
        except exceptions.UserAlreadyExistsError:
            await callback_query.answer(
                'Вы уже зарегистрированы 😬', show_alert=True,
            )
            logger.info(
                'User %d already was registered', callback_query.from_user.id
            )
        else:
            await callback_query.answer(
                'Вы успешно зарегистрировались 🎉', show_alert=True
            )
            logger.info(
                'User %d has been registered', callback_query.from_user.id
            )
            await answer_views(callback_query.message, ShowKeyboardView())


async def register_current_group_chat(
        callback_query: CallbackQuery,
        database_api_http_client_factory: HTTPClientFactory,
):
    logger.debug('Register group chat %d', callback_query.message.chat.id)

    chat_to_create = map_chat_to_create_dto(callback_query.message.chat)

    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)

        try:
            await database_api_service.create_chat(chat_to_create)
        except exceptions.UserAlreadyExistsError:
            await callback_query.answer(
                'Чат уже зарегистрирован 😬', show_alert=True,
            )
            logger.info(
                'Chat %d already was registered', callback_query.message.chat.id
            )
        else:
            await callback_query.answer(
                'Чат успешно зарегистрирован 🎉', show_alert=True,
            )
            logger.info(
                'Chat %d has been registered', callback_query.message.chat.id
            )


async def on_settings_button(
        message: Message,
        database_api_http_client_factory: HTTPClientFactory,
):
    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)
        report_types = await database_api_service.get_role_report_types(
            chat_id=message.from_user.id
        )
    if not report_types:
        await message.answer('У вас нет доступа к отчётам')
    else:
        await answer_views(message, SettingsMenuView(report_types))


async def on_statistics_reports_button(
        message: Message,
        database_api_http_client_factory: HTTPClientFactory,
):
    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)
        report_types = await database_api_service.get_role_report_types(
            chat_id=message.from_user.id
        )
        report_type_names = {report_type.name for report_type in report_types}
        if 'STATISTICS' not in report_type_names:
            await message.answer('У вас нет доступа к отчётам по статистике 😔')
            return
        report_types = await database_api_service.get_statistics_report_types()
    await answer_views(message, StatisticsReportsMenuView(report_types))


async def on_hide_keyboard_command(message: Message):
    await message.answer(
        'Клавиатура спрятана 🙈',
        reply_markup=ReplyKeyboardRemove()
    )


async def on_start(
        message: Message,
        database_api_http_client_factory: HTTPClientFactory,
):
    chat_to_create = map_user_to_create_dto(message.from_user)
    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)
        with contextlib.suppress(exceptions.UserAlreadyExistsError):
            await database_api_service.create_chat(chat_to_create)
    await answer_views(message, ShowKeyboardView())


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(
        register_current_private_chat,
        Text('register_current_chat'),
        chat_type=ChatType.PRIVATE,
        state='*',
    )
    dispatcher.register_callback_query_handler(
        register_current_group_chat,
        Text('register_current_chat'),
        chat_type=(ChatType.GROUP, ChatType.SUPERGROUP),
        state='*',
    )
    dispatcher.register_message_handler(
        on_settings_button,
        Text('⚙️ Настройки') | Command('settings'),
    )
    dispatcher.register_message_handler(
        on_statistics_reports_button,
        Text('📊 Отчёты/Статистика') | Command('reports'),
    )
    dispatcher.register_message_handler(
        on_hide_keyboard_command,
        Command('hide_keyboard'),
    )
    dispatcher.register_message_handler(
        on_start,
        Command('show_keyboard') | CommandStart(),
    )
