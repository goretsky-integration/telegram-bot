import asyncio
from zoneinfo import ZoneInfo

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command

from core import exceptions
from models import Query
from services.auth_api import AuthAPIService, get_tokens_batch
from services.converters import (
    UnitsConverter,
    to_heated_shelf_time_statistics_view_dto
)
from services.database_api import DatabaseAPIService
from services.dodo_api import (
    DodoAPIService,
    get_v2_statistics_reports_batch,
    get_courier_orders,
)
from services.domain.orders import calculate_trips_with_one_order_percentage
from services.http_client_factory import HTTPClientFactory
from services.mappers import group_by_unit_uuid
from services.period import Period
from shortcuts import answer_views, get_message, filter_units_by_ids
from utils.callback_data import show_statistics
from views import HeatedShelfTimeStatisticsView

__all__ = ('register_handlers',)


async def on_heated_shelf_time_statistics_report(
        query: Query,
        dodo_api_http_client_factory: HTTPClientFactory,
        database_api_http_client_factory: HTTPClientFactory,
        auth_api_http_client_factory: HTTPClientFactory,
        country_code: str,
):
    period = Period.today_to_this_time(timezone=ZoneInfo('Europe/Moscow'))
    message = get_message(query)

    report_message = await message.answer('Загрузка')

    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)
        report_type = await database_api_service.get_report_type_by_name(
            name='STATISTICS'
        )
        enabled_unit_ids = await database_api_service.get_report_route_units(
            chat_id=message.chat.id,
            report_type_id=report_type.id,
        )
        if not enabled_unit_ids:
            raise exceptions.NoEnabledUnitsError

        units = await database_api_service.get_role_units(
            chat_id=query.from_user.id,
        )

    units = UnitsConverter(filter_units_by_ids(units, enabled_unit_ids))

    async with auth_api_http_client_factory() as http_client:
        auth_api_service = AuthAPIService(http_client)
        accounts_tokens = await get_tokens_batch(
            auth_api_service=auth_api_service,
            account_names=units.dodo_is_api_account_names,

        )

    async with dodo_api_http_client_factory() as http_client:
        dodo_api_service = DodoAPIService(http_client,
                                          country_code=country_code)

        async with asyncio.TaskGroup() as task_group:
            courier_orders = task_group.create_task(
                get_courier_orders(
                    period=period,
                    units=units,
                    country_code=country_code,
                    dodo_is_api_credentials=accounts_tokens,
                )
            )
            heated_shelf_time_reports = task_group.create_task(
                get_v2_statistics_reports_batch(
                    api_method=dodo_api_service.get_heated_shelf_time_statistics_report,
                    units_grouped_by_account_name=units.grouped_by_dodo_is_api_account_name,
                    accounts_tokens=accounts_tokens,
                )
            )

    courier_orders = courier_orders.result()
    heated_shelf_time_reports = heated_shelf_time_reports.result()

    unit_uuid_to_courier_orders = group_by_unit_uuid(courier_orders)
    unit_uuid_to_trips_with_one_order_percentage = {
        unit_uuid: calculate_trips_with_one_order_percentage(courier_orders)
        for unit_uuid, courier_orders in unit_uuid_to_courier_orders.items()
    }

    units_heated_shelf_time_statistics = to_heated_shelf_time_statistics_view_dto(
        heated_shelf_time_statistics=heated_shelf_time_reports,
        unit_uuid_to_trips_with_one_order_percentage=unit_uuid_to_trips_with_one_order_percentage,
        unit_uuid_to_name=units.unit_uuid_to_name,
    )
    view = HeatedShelfTimeStatisticsView(units_heated_shelf_time_statistics)
    await answer_views(report_message, view, edit=True)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_heated_shelf_time_statistics_report,
        Command('delivery_awaiting_time'),
    )
    dispatcher.register_callback_query_handler(
        on_heated_shelf_time_statistics_report,
        show_statistics.filter(report_type_name='DELIVERY_AWAITING_TIME'),
    )
