import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command

from models import Query
from services.converters import UnitsConverter, to_awaiting_orders_statistics_view_dto
from services.dodo_api import DodoAPIService, get_v1_statistics_reports_batch
from services.database_api import DatabaseAPIService
from services.auth_api import AuthAPIService, get_cookies_batch
from shortcuts import answer_views, get_message, filter_units_by_ids
from utils import logger
from utils.callback_data import show_statistics
from views import AwaitingOrdersStatisticsView

__all__ = ('register_handlers',)


async def on_awaiting_orders_statistics_report(
        query: Query,
        dodo_api_service: DodoAPIService,
        database_api_service: DatabaseAPIService,
        auth_api_service: AuthAPIService,
):
    logger.info('Awaiting orders statistics report request')
    message = get_message(query)
    report_message, units, report_routes = await asyncio.gather(
        message.answer('Загрузка...'),
        database_api_service.get_units(),
        database_api_service.get_reports_routes(chat_id=message.chat.id, report_type='STATISTICS')
    )
    enabled_units_in_current_chat = filter_units_by_ids(units, report_routes[0].unit_ids)

    units = UnitsConverter(enabled_units_in_current_chat)
    accounts_cookies = await get_cookies_batch(auth_api_service=auth_api_service, account_names=units.account_names)
    reports = await get_v1_statistics_reports_batch(
        api_method=dodo_api_service.get_awaiting_orders_statistics_report,
        accounts_cookies=accounts_cookies,
        units_grouped_by_account_name=units.grouped_by_account_name,
    )
    awaiting_orders_statistics = to_awaiting_orders_statistics_view_dto(reports, units.unit_id_to_name)
    view = AwaitingOrdersStatisticsView(awaiting_orders_statistics=awaiting_orders_statistics)
    await answer_views(report_message, view, edit=True)
    logger.info('Awaiting orders statistics report sent')


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_awaiting_orders_statistics_report,
        Command('awaiting_orders'),
    )
    dispatcher.register_callback_query_handler(
        on_awaiting_orders_statistics_report,
        show_statistics.filter(report_type_name='AWAITING_ORDERS'),
    )
