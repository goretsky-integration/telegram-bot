from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

import db
import models.database
import responses
from bot import dp
from services import filters, api, statistics
from utils import callback_data as cd
from utils.helpers import group_units_by_account_name


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.DAILY_REVENUE.name),
    filters.EnabledUnitIdsFilter(),
)
async def on_update_daily_revenue_query(
        callback_query: CallbackQuery,
        enabled_unit_ids: list[int],
):
    units = await db.get_units()
    unit_id_to_name = {unit.id: unit.name for unit in units}
    revenue_statistics = await api.get_revenue_statistics(enabled_unit_ids)
    response = responses.RevenueStatistics(revenue_statistics, unit_id_to_name)
    await callback_query.message.edit_text(**response.as_dict())


@dp.message_handler(
    Command(models.StatisticsReportType.DAILY_REVENUE.name),
    filters.EnabledUnitIdsFilter(),
)
async def on_statistics_report_command(message: Message, enabled_unit_ids: list[int]):
    skeleton_message = await message.answer('<i>Загрузка...</i>')
    units = await db.get_units()
    unit_id_to_name = {unit.id: unit.name for unit in units}
    revenue_statistics = await api.get_revenue_statistics(enabled_unit_ids)
    response = responses.RevenueStatistics(revenue_statistics, unit_id_to_name)
    await skeleton_message.edit_text(**response.as_dict())


@dp.message_handler(
    Command(models.StatisticsReportType.KITCHEN_PERFORMANCE.name),
    filters.EnabledUnitIdsFilter(),
)
async def on_kitchen_performance_command(message: Message, enabled_unit_ids: list[int]):
    skeleton_message = await message.answer('<i>Загрузка...</i>')
    units = [unit for unit in await db.get_units() if unit.id in enabled_unit_ids]
    unit_id_to_name = {unit.id: unit.name for unit in units}
    kitchen_statistics = await statistics.get_kitchen_statistics(units)
    response = responses.KitchenStatistics(kitchen_statistics, unit_id_to_name)
    await skeleton_message.edit_text(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.KITCHEN_PERFORMANCE.name),
    filters.EnabledUnitIdsFilter(),
)
async def on_update_kitchen_performance_query(callback_query: CallbackQuery, enabled_unit_ids: list[int]):
    units = [unit for unit in await db.get_units() if unit.id in enabled_unit_ids]
    unit_id_to_name = {unit.id: unit.name for unit in units}
    kitchen_statistics = await statistics.get_kitchen_statistics(units)
    response = responses.KitchenStatistics(kitchen_statistics, unit_id_to_name)
    await callback_query.message.edit_text(**response.as_dict())
