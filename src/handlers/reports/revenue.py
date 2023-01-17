import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command

from models import Query
from services import converters
from services.database_api import DatabaseAPIService
from services.dodo_api import DodoAPIService
from shortcuts import get_message, answer_views
from utils import logger
from utils.callback_data import show_statistics
from views import RevenueStatisticsView

__all__ = ('register_handlers',)


async def on_daily_revenue_statistics_report(
        query: Query,
        dodo_api_service: DodoAPIService,
        database_api_service: DatabaseAPIService,
) -> None:
    logger.info('Revenue statistics report request')
    message = get_message(query)
    report_message, units, report_routes = await asyncio.gather(
        message.answer('Загрузка...'),
        database_api_service.get_units(),
        database_api_service.get_reports_routes(chat_id=message.chat.id, report_type='STATISTICS'),
    )
    revenue_statistics = await dodo_api_service.get_revenue_statistics_report(report_routes[0].unit_ids)
    unit_id_to_name = {unit.id: unit.name for unit in units}
    revenue_statistics_view_dto = converters.to_revenue_statistics_view_dto(revenue_statistics, unit_id_to_name)
    view = RevenueStatisticsView(revenue_statistics_view_dto)
    await answer_views(report_message, view, edit=True)
    logger.info('Revenue statistics report sent')


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_daily_revenue_statistics_report,
        Command('daily_revenue'),
    )
    dispatcher.register_callback_query_handler(
        on_daily_revenue_statistics_report,
        show_statistics.filter(report_type_name='DAILY_REVENUE'),
    )
