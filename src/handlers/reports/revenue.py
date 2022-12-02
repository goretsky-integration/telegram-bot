import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from dodolib import DodoAPIClient, DatabaseClient
from dodolib.utils.convert_models import UnitsConverter

from models import Query
from shortcuts import get_message, validate_reports, answer_views
from utils import logger
from utils.callback_data import show_statistics
from views import RevenueStatisticsView

__all__ = ('register_handlers',)


async def on_daily_revenue_statistics_report(query: Query, api_client: DodoAPIClient, db_client: DatabaseClient):
    logger.debug('New report request')
    message = get_message(query)
    report_message = await message.answer('Загрузка...')
    units, reports = await asyncio.gather(
        db_client.get_units(),
        db_client.get_reports(chat_id=message.chat.id, report_type='STATISTICS'),
    )
    validate_reports(reports)
    revenue_statistics = await api_client.get_revenue_statistics('ru', reports[0].unit_ids)
    view = RevenueStatisticsView(revenue_statistics, UnitsConverter(units).ids_to_names)
    await answer_views(report_message, view, edit=True)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_daily_revenue_statistics_report,
        Command('daily_revenue'),
    )
    dispatcher.register_callback_query_handler(
        on_daily_revenue_statistics_report,
        show_statistics.filter(report_type_name='DAILY_REVENUE'),
    )
