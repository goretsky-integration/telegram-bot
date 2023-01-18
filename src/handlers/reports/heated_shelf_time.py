import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command

from models import Query
from services.auth_api import AuthAPIService, get_tokens_batch, get_cookies_batch
from services.converters import UnitsConverter, to_heated_shelf_time_statistics_view_dto
from services.database_api import DatabaseAPIService
from services.dodo_api import DodoAPIService, get_v2_statistics_reports_batch, get_v1_statistics_reports_batch
from shortcuts import answer_views, get_message, filter_units_by_ids, flatten
from utils import logger
from utils.callback_data import show_statistics
from views import HeatedShelfTimeStatisticsView

__all__ = ('register_handlers',)


async def on_heated_shelf_time_statistics_report(
        query: Query,
        dodo_api_service: DodoAPIService,
        database_api_service: DatabaseAPIService,
        auth_api_service: AuthAPIService,
):
    logger.info('Heated shelf time statistics report request')
    message = get_message(query)
    report_message, units, reports = await asyncio.gather(
        message.answer('Загрузка...'),
        database_api_service.get_units(),
        database_api_service.get_reports_routes(chat_id=message.chat.id, report_type='STATISTICS'),
    )
    units = UnitsConverter(filter_units_by_ids(units, reports[0].unit_ids))
    accounts_cookies, accounts_tokens = await asyncio.gather(
        get_cookies_batch(auth_api_service=auth_api_service, account_names=units.account_names),
        get_tokens_batch(auth_api_service=auth_api_service, account_names=units.account_names),
    )
    trips_with_one_order_reports, heated_shelf_time_reports = await asyncio.gather(
        get_v1_statistics_reports_batch(
            api_method=dodo_api_service.get_trips_with_one_order_statistics_report,
            units_grouped_by_account_name=units.grouped_by_account_name,
            accounts_cookies=accounts_cookies,
        ),
        get_v2_statistics_reports_batch(
            api_method=dodo_api_service.get_heated_shelf_time_statistics_report,
            units_grouped_by_account_name=units.grouped_by_account_name,
            accounts_tokens=accounts_tokens,
        )
    )
    units_heated_shelf_time_statistics = to_heated_shelf_time_statistics_view_dto(
        heated_shelf_time_statistics=heated_shelf_time_reports,
        trips_with_one_order_statistics=flatten(trips_with_one_order_reports),
        unit_uuid_to_name=units.unit_uuid_to_name,
    )
    view = HeatedShelfTimeStatisticsView(units_heated_shelf_time_statistics)
    await answer_views(report_message, view, edit=True)
    logger.info('Heated shelf time statistics report sent')


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_heated_shelf_time_statistics_report,
        Command('delivery_awaiting_time'),
    )
    dispatcher.register_callback_query_handler(
        on_heated_shelf_time_statistics_report,
        show_statistics.filter(report_type_name='DELIVERY_AWAITING_TIME'),
    )
