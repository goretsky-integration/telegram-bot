from aiogram.types import CallbackQuery

import models
import db
import responses
from bot import dp
from utils import callback_data as cd


@dp.callback_query_handler(cd.switch_all_unit_statuses.filter())
async def on_switch_all_unit_statuses_button(
        callback_query: CallbackQuery,
        callback_data: models.AllUnitIdsByRegionCallbackData,
):
    region = callback_data['region']
    report_type = callback_data['report_type']
    action = callback_data['action']
    chat_id = callback_query.message.chat.id

    units_by_region = await db.get_units_by_region(region)
    unit_ids_by_region = [unit.id for unit in units_by_region]

    match action:
        case 'enable':
            await db.insert_unit_by_report_type_and_chat_id(report_type, chat_id, unit_ids_by_region)
        case 'disable':
            await db.delete_unit_by_report_type_and_chat_id(report_type, chat_id, unit_ids_by_region)
        case _:
            raise ValueError('Unknown action type')

    enabled_unit_ids = await db.get_unit_ids_by_report_type_and_chat_id(report_type, chat_id)
    enabled_unit_ids_by_region = set(unit_ids_by_region) & set(enabled_unit_ids)
    response = responses.UnitsResponse(report_type, region, enabled_unit_ids_by_region, units_by_region)

    await callback_query.message.edit_text(**response.as_dict())
    await callback_query.answer()


@dp.callback_query_handler(cd.switch_unit_status.filter())
async def on_switch_unit_statis_button(
        callback_query: CallbackQuery,
        callback_data: models.SwitchUnitStatusCallbackData,
):
    is_unit_enabled = bool(int(callback_data['is_unit_enabled']))
    unit_id = int(callback_data['unit_id'])
    report_type = callback_data['report_type']
    region = callback_data['region']

    if is_unit_enabled:
        await db.delete_unit_by_report_type_and_chat_id(report_type, callback_query.message.chat.id, [unit_id])
    else:
        await db.insert_unit_by_report_type_and_chat_id(report_type, callback_query.message.chat.id, [unit_id])
    units_by_region = await db.get_units_by_region(region)
    unit_ids_by_region = {unit.id for unit in units_by_region}
    enabled_unit_ids = await db.get_unit_ids_by_report_type_and_chat_id(report_type, callback_query.message.chat.id)
    enabled_unit_ids_by_region = unit_ids_by_region & set(enabled_unit_ids)
    response = responses.UnitsResponse(report_type, region, enabled_unit_ids_by_region, units_by_region)
    await callback_query.message.edit_text(**response.as_dict())


@dp.callback_query_handler(cd.units_by_region.filter())
async def on_region_units_button(
        callback_query: CallbackQuery,
        callback_data: models.UnitsByRegionCallbackData,
):
    report_type = callback_data['report_type']
    region = callback_data['region']
    all_units = await db.get_units_by_region(region)
    enabled_unit_ids = await db.get_unit_ids_by_report_type_and_chat_id(report_type, callback_query.message.chat.id)
    response = responses.UnitsResponse(report_type, region, enabled_unit_ids, all_units)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.callback_query_handler(cd.report_settings.filter())
async def on_statistics_settings_button(
        callback_query: CallbackQuery,
        callback_data: models.ReportTypeCallbackData,
):
    regions = await db.get_regions()
    report_type = callback_data['name']
    response = responses.RegionsResponse(report_type, regions)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()
