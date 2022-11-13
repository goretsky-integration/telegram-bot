from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text, Command, CommandStart
from aiogram.types import Message
from dodolib import DatabaseClient

import responses

__all__ = ('register_handlers',)


async def on_settings_button(message: Message, db_client: DatabaseClient):
    report_types = await db_client.get_report_types()
    await message.answer(**responses.SettingsMenu(report_types).as_dict())


async def on_statistics_reports_button(message: Message, db_client: DatabaseClient):
    statistics_report_types = await db_client.get_statistics_report_types()
    await message.answer(**responses.StatisticsReportsMenu(statistics_report_types).as_dict())


async def on_hide_keyboard_command(message: Message):
    await message.reply(**responses.HideKeyboard().as_dict())


async def on_start(message: Message):
    await message.reply(**responses.ShowKeyboard().as_dict())


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
