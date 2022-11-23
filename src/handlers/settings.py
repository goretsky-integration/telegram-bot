from aiogram import Dispatcher
from aiogram.types import CallbackQuery
from dodolib import DatabaseClient

import models
from shortcuts import answer_views
from utils import callback_data as cd

__all__ = ('register_handlers',)

from views import UnitsResponseView, RegionsResponseView


async def on_switch_all_unit_statuses_button(
        callback_query: CallbackQuery,
        callback_data: models.AllUnitIdsByRegionCallbackData,
        db_client: DatabaseClient,
):
    region = callback_data['region']
    report_type = callback_data['report_type']
    action = callback_data['action']
    chat_id = callback_query.message.chat.id

    units_by_region = await db_client.get_units(region=region)
    unit_ids_by_region = [unit.id for unit in units_by_region]

    match action:
        case 'enable':
            await db_client.add_unit_ids_to_report(report_type, chat_id, unit_ids_by_region)
        case 'disable':
            await db_client.remove_unit_ids_from_report(report_type, chat_id, unit_ids_by_region)

    enabled_reports = await db_client.get_reports(report_type=report_type, chat_id=chat_id)
    enabled_unit_ids = [unit_id for report in enabled_reports for unit_id in report.unit_ids]
    enabled_unit_ids_by_region = set(unit_ids_by_region) & set(enabled_unit_ids)
    response = UnitsResponseView(report_type, region, enabled_unit_ids_by_region, units_by_region)
    await answer_views(callback_query.message, response)
    await callback_query.answer()


async def on_switch_unit_statis_button(
        callback_query: CallbackQuery,
        callback_data: models.SwitchUnitStatusCallbackData,
        db_client: DatabaseClient,
):
    is_unit_enabled = bool(int(callback_data['is_unit_enabled']))
    unit_id = int(callback_data['unit_id'])
    report_type = callback_data['report_type']
    region = callback_data['region']

    if is_unit_enabled:
        await db_client.remove_unit_ids_from_report(report_type, callback_query.message.chat.id, [unit_id])
    else:
        await db_client.add_unit_ids_to_report(report_type, callback_query.message.chat.id, [unit_id])
    units_by_region = await db_client.get_units(region)
    unit_ids_by_region = {unit.id for unit in units_by_region}
    enabled_reports = await db_client.get_reports(report_type=report_type, chat_id=callback_query.message.chat.id)
    enabled_unit_ids = [unit_id for report in enabled_reports for unit_id in report.unit_ids]
    enabled_unit_ids_by_region = unit_ids_by_region & set(enabled_unit_ids)
    response = UnitsResponseView(report_type, region, enabled_unit_ids_by_region, units_by_region)
    await answer_views(callback_query.message, response)


async def on_region_units_button(
        callback_query: CallbackQuery,
        callback_data: models.UnitsByRegionCallbackData,
        db_client: DatabaseClient,
):
    report_type = callback_data['report_type_name']
    region = callback_data['region']
    all_units = await db_client.get_units(region)
    enabled_units = await db_client.get_reports(report_type=report_type, chat_id=callback_query.message.chat.id)
    enabled_unit_ids = [unit_id for report in enabled_units for unit_id in report.unit_ids]
    response = UnitsResponseView(report_type, region, enabled_unit_ids, all_units)
    await answer_views(callback_query.message, response)
    await callback_query.answer()


async def on_statistics_settings_button(
        callback_query: CallbackQuery,
        callback_data: models.ReportTypeCallbackData,
        db_client: DatabaseClient,
):
    report_type = callback_data['report_type_name']
    regions = await db_client.get_regions()
    response = RegionsResponseView(report_type, regions)
    await answer_views(callback_query.message, response)
    await callback_query.answer()


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(
        on_switch_all_unit_statuses_button,
        cd.switch_all_unit_statuses.filter()
    )
    dispatcher.register_callback_query_handler(
        on_switch_unit_statis_button,
        cd.switch_unit_status.filter(),
    )
    dispatcher.register_callback_query_handler(
        on_region_units_button,
        cd.units_by_region.filter(),
    )
    dispatcher.register_callback_query_handler(
        on_statistics_settings_button,
        cd.report_settings.filter(),
    )
