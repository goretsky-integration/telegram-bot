from aiogram.dispatcher.filters import Text, Command
from aiogram.types import Message

import responses
from bot import dp


@dp.message_handler(Command('settings'))
@dp.message_handler(Text('⚙️ Настройки'))
async def on_settings_button(message: Message):
    await message.answer(**responses.SettingsMenu().as_dict())


@dp.message_handler(Command('reports'))
@dp.message_handler(Text('📊 Отчёты/Статистика'))
async def on_statistics_reports_button(message: Message):
    await message.answer(**responses.StatisticsReportsMenu().as_dict())


@dp.message_handler()
async def on_start(message: Message):
    await message.answer(**responses.MainMenu().as_dict())
