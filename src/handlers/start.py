from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, Command, CommandStart
from aiogram.types import Message, ReplyKeyboardRemove

from services.database_api import DatabaseAPIService
from shortcuts import answer_views
from views import (
    SettingsMenuView,
    StatisticsReportsMenuView,
    ShowKeyboardView,
)

__all__ = ('register_handlers',)


async def on_settings_button(message: Message, database_api_service: DatabaseAPIService):
    report_types = await database_api_service.get_report_types()
    await answer_views(message, SettingsMenuView(report_types))


async def on_statistics_reports_button(message: Message, database_api_service: DatabaseAPIService):
    report_types = await database_api_service.get_statistics_report_types()
    await answer_views(message, StatisticsReportsMenuView(report_types))


async def on_hide_keyboard_command(message: Message):
    await message.answer(
        'Клавиатура спрятана 🙈',
        reply_markup=ReplyKeyboardRemove()
    )


async def on_start(message: Message):
    await answer_views(message, ShowKeyboardView())


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_settings_button,
        Text('⚙️ Настройки'),
    )
    dispatcher.register_message_handler(
        on_settings_button,
        Command('settings'),
    )
    dispatcher.register_message_handler(
        on_statistics_reports_button,
        Command('reports'),
    )
    dispatcher.register_message_handler(
        on_statistics_reports_button,
        Text('📊 Отчёты/Статистика'),
    )
    dispatcher.register_message_handler(
        on_hide_keyboard_command,
        Command('hide_keyboard'),
    )
    dispatcher.register_message_handler(
        on_start,
        Command('show_keyboard'),
    )
    dispatcher.register_message_handler(
        on_start,
        CommandStart(),
    )
