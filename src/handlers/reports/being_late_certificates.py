import asyncio
import logging

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command

from models import Query
from services.auth_api import AuthAPIService, get_tokens_batch
from services.converters import UnitsConverter, to_late_delivery_vouchers_statistics_view_dto
from services.database_api import DatabaseAPIService
from services.dodo_api import DodoAPIService, get_v2_statistics_reports_batch
from shortcuts import answer_views, get_message, filter_units_by_ids, validate_report_routes
from utils.callback_data import show_statistics
from views import BeingLateCertificatesStatisticsView

__all__ = ('register_handlers',)


async def on_being_late_certificates_statistics_report(
        query: Query,
        dodo_api_service: DodoAPIService,
        database_api_service: DatabaseAPIService,
        auth_api_service: AuthAPIService,
):
    logging.debug('New report request')
    message = get_message(query)
    report_message, units, report_routes = await asyncio.gather(
        message.answer('Загрузка...'),
        database_api_service.get_units(),
        database_api_service.get_reports_routes(chat_id=message.chat.id, report_type='STATISTICS'),
    )
    validate_report_routes(report_routes)
    units = UnitsConverter(filter_units_by_ids(units, report_routes[0].unit_ids))
    accounts_tokens = await get_tokens_batch(auth_api_service=auth_api_service, account_names=units.account_names)
    reports = await get_v2_statistics_reports_batch(
        api_method=dodo_api_service.get_late_delivery_vouchers_statistics_report,
        units_grouped_by_account_name=units.grouped_by_account_name,
        accounts_tokens=accounts_tokens,
    )
    late_delivery_vouchers_statistics = to_late_delivery_vouchers_statistics_view_dto(reports, units.unit_uuid_to_name)
    view = BeingLateCertificatesStatisticsView(late_delivery_vouchers_statistics)
    await answer_views(report_message, view, edit=True)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_being_late_certificates_statistics_report,
        Command('being_late_certificates'),
    )
    dispatcher.register_callback_query_handler(
        on_being_late_certificates_statistics_report,
        show_statistics.filter(report_type_name='BEING_LATE_CERTIFICATES'),
    )
