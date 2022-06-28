from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

import db
import models.database
from bot import dp
from services import statistics_reports
from utils import callback_data as cd


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.DAILY_REVENUE.name))
async def on_update_daily_revenue_query(
        callback_query: CallbackQuery,
        callback_data: models.StatisticsReportTypeCallbackData,
):
    report_type = callback_data['name']
    units = await db.get_units()
    unit_id_to_name = {unit.id: unit.name for unit in units}
    daily_revenue_strategy = statistics_reports.report_type_to_strategy[report_type]
    strategy = daily_revenue_strategy(report_type, callback_query.message.chat.id, unit_id_to_name)
    response = await strategy.get_statistics_report()
    await callback_query.message.edit_text(**response.as_dict())


@dp.message_handler(
    Command(models.StatisticsReportType.DAILY_REVENUE.name)
)
async def on_daily_revenue_command(message: Message, command: Command.CommandObj):
    report_type = command.command.upper()
    skeleton_message = await message.answer('<i>Загрузка...</i>')
    units = await db.get_units()
    unit_id_to_name = {unit.id: unit.name for unit in units}
    daily_revenue_strategy = statistics_reports.report_type_to_strategy[report_type]
    strategy = daily_revenue_strategy(report_type, message.chat.id, unit_id_to_name)
    response = await strategy.get_statistics_report()
    await skeleton_message.edit_text(**response.as_dict())
