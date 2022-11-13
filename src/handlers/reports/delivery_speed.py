import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from dodolib import DatabaseClient, AuthClient, DodoAPIClient
from dodolib.utils.convert_models import UnitsConverter

from models import Query
from shortcuts import answer_views, validate_reports, get_message, get_accounts_tokens_batch, \
    get_statistics_report_by_tokens_batch
from utils import logger
from utils.callback_data import show_statistics
from views import DeliverySpeedStatisticsView

__all__ = ('register_handlers',)


async def on_delivery_speed_statistics_report(
        query: Query,
        api_client: DodoAPIClient,
        auth_client: AuthClient,
        db_client: DatabaseClient,
):
    logger.debug('New report request')
    message = get_message(query)
    units, reports = await asyncio.gather(
        db_client.get_units(),
        db_client.get_reports(chat_id=message.chat.id, report_type='STATISTICS'),
    )
    validate_reports(reports)
    units = UnitsConverter(units)
    accounts_tokens = await get_accounts_tokens_batch(auth_client, units.account_names)
    units_statistics = await get_statistics_report_by_tokens_batch(
        api_client.get_delivery_speed_statistics,
        units.account_names_to_unit_uuids,
        accounts_tokens,
    )
    view = DeliverySpeedStatisticsView(units_statistics, units.uuid_to_name())
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_delivery_speed_statistics_report,
        Command('delivery_speed'),
    )
    dispatcher.register_callback_query_handler(
        on_delivery_speed_statistics_report,
        show_statistics.filter(report_type_name='DELIVERY_SPEED'),
    )
