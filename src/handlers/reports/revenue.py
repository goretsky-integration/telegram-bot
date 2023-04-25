from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command

from core import exceptions
from models import Query
from services import converters
from services.database_api import DatabaseAPIService
from services.dodo_api import DodoAPIService
from services.http_client_factory import HTTPClientFactory
from shortcuts import (
    get_message, edit_message_by_view
)
from utils.callback_data import show_statistics
from views import RevenueStatisticsView

__all__ = ('register_handlers',)


async def on_daily_revenue_statistics_report(
        query: Query,
        country_code: str,
        dodo_api_http_client_factory: HTTPClientFactory,
        database_api_http_client_factory: HTTPClientFactory,
) -> None:
    message = get_message(query)
    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)

        report_type = await database_api_service.get_report_type_by_name(
            name='STATISTICS',
        )
        units = await database_api_service.get_role_units(
            chat_id=query.from_user.id,
        )
        unit_ids = await database_api_service.get_report_route_units(
            chat_id=message.chat.id,
            report_type_id=report_type.id,
        )
    if not unit_ids:
        raise exceptions.NoEnabledUnitsError

    report_message = await message.answer('Загрузка...')

    async with dodo_api_http_client_factory() as http_client:
        dodo_api_service = DodoAPIService(http_client, country_code)
        revenue_statistics = await dodo_api_service.get_revenue_statistics_report(unit_ids)

    unit_id_to_name = {unit.id: unit.name for unit in units}
    revenue_statistics_view_dto = converters.to_revenue_statistics_view_dto(
        revenue_statistics, unit_id_to_name)
    view = RevenueStatisticsView(revenue_statistics_view_dto)
    await edit_message_by_view(report_message, view)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_daily_revenue_statistics_report,
        Command('daily_revenue'),
    )
    dispatcher.register_callback_query_handler(
        on_daily_revenue_statistics_report,
        show_statistics.filter(report_type_name='DAILY_REVENUE'),
    )
