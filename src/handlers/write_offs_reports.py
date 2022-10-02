from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, CallbackQuery

from bot import dp
from responses import WriteOffsReportPeriodResponse
from services import periods
from utils import logger
from utils.callback_data import prepopulated_period


@dp.callback_query_handler(Text('other-period'), state='*')
async def on_other_write_offs_period(callback_query: CallbackQuery):
    await callback_query.answer('В разработке 🏗', show_alert=True)


@dp.callback_query_handler(
    prepopulated_period.filter(period=['last-7-days', 'last-14-days', 'last-30-days']),
    state='*',
)
async def on_prepopulated_write_offs_periods(callback_query: CallbackQuery, callback_data: dict):
    period = callback_data['period']
    period_to_callback = {
        'last-7-days': periods.get_last_7_days_period,
        'last-14-days': periods.get_last_14_days_period,
        'last-30-days': periods.get_last_30_days_period,
    }
    get_period = period_to_callback[period]
    logger.debug(f'Period {period}')
    await callback_query.answer('В разработке 🏗', show_alert=True)


@dp.message_handler(Command('write_offs_report'), state='*')
async def on_reports_button(message: Message):
    return await message.answer(**WriteOffsReportPeriodResponse().as_dict())
