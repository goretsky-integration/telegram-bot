import asyncio

import httpx
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from dodo_is_api import models as dodo_is_api_models

from core import exceptions
from models import Query
from services.auth_api import AuthAPIService, get_tokens_batch
from services.converters import UnitsConverter
from services.database_api import DatabaseAPIService
from services.dodo_api import (
    get_late_delivery_vouchers_for_today_and_week_before
)
from services.domain.vouchers import (
    calculate_late_delivery_vouchers_count_for_today_and_week_before,
)
from services.http_client_factory import HTTPClientFactory
from shortcuts import answer_views, get_message, filter_units_by_ids
from utils.callback_data import show_statistics
from views import BeingLateCertificatesStatisticsView

__all__ = ('register_handlers',)


async def on_being_late_certificates_statistics_report(
        query: Query,
        database_api_http_client_factory: HTTPClientFactory,
        auth_api_http_client_factory: HTTPClientFactory,
        country_code: dodo_is_api_models.CountryCode,
):
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

    async with httpx.AsyncClient() as http_client:
        vouchers_for_today, vouchers_for_week_before = (
            await get_late_delivery_vouchers_for_today_and_week_before(
                units=units,
                country_code=country_code,
                http_client=http_client,
                dodo_is_api_credentials=accounts_tokens,
            )
        )

    units_late_delivery_vouchers_for_today_and_week_before = (
        calculate_late_delivery_vouchers_count_for_today_and_week_before(
            unit_uuid_to_name=units.unit_uuid_to_name,
            vouchers_for_today=vouchers_for_today,
            vouchers_for_week_before=vouchers_for_week_before,
        )
    )
    view = BeingLateCertificatesStatisticsView(
        units_late_delivery_vouchers_for_today_and_week_before,
    )
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
