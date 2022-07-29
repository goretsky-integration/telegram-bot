from aiogram.dispatcher.filters import Text, Command, CommandStart
from aiogram.types import Message

import responses
from bot import dp
from repositories import DatabaseRepository


@dp.message_handler(Command('settings'))
@dp.message_handler(Text('⚙️ Настройки'))
async def on_settings_button(message: Message, db: DatabaseRepository):
    report_types = await db.get_report_types()
    await message.answer(**responses.SettingsMenu(report_types).as_dict())


@dp.message_handler(Command('reports'))
@dp.message_handler(Text('📊 Отчёты/Статистика'))
async def on_statistics_reports_button(message: Message, db: DatabaseRepository):
    statistics_report_types = await db.get_statistics_report_types()
    await message.answer(**responses.StatisticsReportsMenu(statistics_report_types).as_dict())


@dp.message_handler(CommandStart())
async def on_start(message: Message):
    await message.answer(**responses.MainMenu().as_dict())
