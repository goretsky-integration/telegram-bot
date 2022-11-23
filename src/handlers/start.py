from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, Command, CommandStart
from aiogram.types import Message
from dodolib import DatabaseClient

from shortcuts import answer_views
from views import SettingsMenuView, StatisticsReportsMenuView, HideKeyboardView, ShowKeyboardView

__all__ = ('register_handlers',)


async def on_settings_button(message: Message, db_client: DatabaseClient):
    report_types = await db_client.get_report_types()
    await answer_views(message, SettingsMenuView(report_types))


async def on_statistics_reports_button(message: Message, db_client: DatabaseClient):
    statistics_report_types = await db_client.get_statistics_report_types()
    await answer_views(message, StatisticsReportsMenuView(statistics_report_types))


async def on_hide_keyboard_command(message: Message):
    await answer_views(message, HideKeyboardView())


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
