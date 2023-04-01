import asyncio

from aiogram import Dispatcher
from aiogram.types import CallbackQuery

import models
from services.database_api import DatabaseAPIService
from services.http_client_factory import HTTPClientFactory
from shortcuts import answer_views, edit_message_by_view
from utils import callback_data as cd
from views import UnitsResponseView, RegionsResponseView

__all__ = ('register_handlers',)


async def on_switch_all_unit_statuses_button(
        callback_query: CallbackQuery,
        callback_data: models.AllUnitIdsByRegionCallbackData,
        database_api_http_client_factory: HTTPClientFactory,
):
    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)
        units = await database_api_service.get_role_units(
            region_id=callback_data['region_id'],
            chat_id=callback_query.from_user.id,
        )

        enabled_unit_ids = await database_api_service.get_report_route_units(
            chat_id=callback_query.from_user.id,
            report_type_id=callback_data['report_type_id']
        )

        if callback_data['action'] == 'disable':
            method = database_api_service.delete_report_routes
            unit_ids_for_request = enabled_unit_ids
        else:
            method = database_api_service.create_report_routes
            unit_ids_for_request = {
                unit.id for unit in units
                if unit.id not in enabled_unit_ids
            }
        await method(
            report_type_id=callback_data['report_type_id'],
            chat_id=callback_query.from_user.id,
            unit_ids=unit_ids_for_request,
        )

        enabled_unit_ids = await database_api_service.get_report_route_units(
            chat_id=callback_query.from_user.id,
            report_type_id=callback_data['report_type_id']
        )

    response = UnitsResponseView(
        report_type_id=callback_data['report_type_id'],
        region_id=callback_data['region_id'],
        enabled_unit_ids=enabled_unit_ids,
        all_units=units,
    )
    await edit_message_by_view(callback_query.message, response)
    await callback_query.answer()


async def on_switch_unit_statis_button(
        callback_query: CallbackQuery,
        callback_data: models.SwitchUnitStatusCallbackData,
        database_api_http_client_factory: HTTPClientFactory,
):
    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)

        method = (
            database_api_service.delete_report_routes
            if callback_data['is_unit_enabled']
            else database_api_service.create_report_routes
        )
        await method(
            report_type_id=callback_data['report_type_id'],
            chat_id=callback_query.from_user.id,
            unit_ids=(callback_data['unit_id'],)
        )

        units = await database_api_service.get_role_units(
            chat_id=callback_query.from_user.id,
            region_id=callback_data['region_id'],
        )
        enabled_unit_ids = await database_api_service.get_report_route_units(
            chat_id=callback_query.from_user.id,
            report_type_id=callback_data['report_type_id'],
        )

    response = UnitsResponseView(
        report_type_id=callback_data['report_type_id'],
        region_id=callback_data['region_id'],
        enabled_unit_ids=enabled_unit_ids,
        all_units=units,
    )
    await edit_message_by_view(callback_query.message, response)


async def on_region_units_button(
        callback_query: CallbackQuery,
        callback_data: models.UnitsByRegionCallbackData,
        database_api_http_client_factory: HTTPClientFactory,
):
    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)

        async with asyncio.TaskGroup() as task_group:
            units = task_group.create_task(
                database_api_service.get_role_units(
                    chat_id=callback_query.from_user.id,
                    region_id=callback_data['region_id'],
                ),
            )
            report_routes_unit_ids = task_group.create_task(
                database_api_service.get_report_route_units(
                    chat_id=callback_query.from_user.id,
                    report_type_id=callback_data['report_type_id'],
                ),
            )
    units = units.result()
    report_routes_unit_ids = report_routes_unit_ids.result()

    response = UnitsResponseView(
        report_type_id=callback_data['report_type_id'],
        region_id=callback_data['region_id'],
        enabled_unit_ids=report_routes_unit_ids,
        all_units=units,
    )
    await edit_message_by_view(callback_query.message, response)
    await callback_query.answer()


async def show_report_type_regions_menu(
        callback_query: CallbackQuery,
        callback_data: models.ReportTypeCallbackData,
        database_api_http_client_factory: HTTPClientFactory,
):
    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)
        regions = await database_api_service.get_role_regions(
            chat_id=callback_query.from_user.id,
        )
    report_type_id = callback_data['report_type_id']

    response = RegionsResponseView(report_type_id, regions)
    await answer_views(callback_query.message, response)
    await callback_query.answer()


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_callback_query_handler(
        on_switch_all_unit_statuses_button,
        cd.SwitchAllUnitStatusesCallbackData().filter()
    )
    dispatcher.register_callback_query_handler(
        on_switch_unit_statis_button,
        cd.SwitchUnitStatusCallbackData().filter(),
    )
    dispatcher.register_callback_query_handler(
        on_region_units_button,
        cd.UnitsByRegionCallbackData().filter(),
    )
    dispatcher.register_callback_query_handler(
        show_report_type_regions_menu,
        cd.ReportSettingsCallbackData().filter(),
    )
