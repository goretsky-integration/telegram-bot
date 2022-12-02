import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from dodolib import models, DatabaseClient, AuthClient, DodoAPIClient
from dodolib.utils.convert_models import UnitsConverter

from models import Query
from shortcuts import answer_views, validate_reports, get_message, filter_units_by_ids
from utils import logger
from utils.callback_data import show_statistics
from views import TotalCookingTimeStatisticsView, AwaitingOrdersStatisticsView

__all__ = ('register_handlers',)


async def on_awaiting_orders_statistics_report(
        query: Query,
        api_client: DodoAPIClient,
        auth_client: AuthClient,
        db_client: DatabaseClient,
):
    logger.debug('New report request')
    message = get_message(query)
    report_message = await message.answer('Загрузка...')
    units, reports = await asyncio.gather(
        db_client.get_units(),
        db_client.get_reports(chat_id=message.chat.id, report_type='STATISTICS'),
    )
    validate_reports(reports)
    units = UnitsConverter(filter_units_by_ids(units, reports[0].unit_ids))
    tasks = (auth_client.get_cookies(account_name) for account_name in units.account_names)
    accounts_cookies = await asyncio.gather(*tasks)
    account_name_to_unit_ids = units.account_names_to_unit_ids
    tasks = (api_client.get_partial_delivery_statistics(account_cookies.cookies,
                                                        account_name_to_unit_ids[account_cookies.account_name])
             for account_cookies in accounts_cookies)
    units_statistics: tuple[models.DeliveryPartialStatisticsReport, ...] = await asyncio.gather(*tasks)
    results = []
    errors = []
    for unit in units_statistics:
        results += unit.results
        errors += unit.errors
    view = AwaitingOrdersStatisticsView(
        models.DeliveryPartialStatisticsReport(results=results, errors=errors),
        units.ids_to_names,
    )
    await answer_views(report_message, view, edit=True)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_awaiting_orders_statistics_report,
        Command('awaiting_orders'),
    )
    dispatcher.register_callback_query_handler(
        on_awaiting_orders_statistics_report,
        show_statistics.filter(report_type_name='AWAITING_ORDERS'),
    )
