import httpx
from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from dodo_is_api.models import CountryCode

from core import exceptions
from services.auth_api import get_cookies_batch, AuthAPIService
from services.converters import UnitsConverter
from services.database_api import DatabaseAPIService
from services.dodo_api import get_units_kitchen_operational_statistics
from services.domain.operational_statistics import \
    calculate_restaurant_average_pending_and_cooking_time
from services.http_client_factory import HTTPClientFactory
from shortcuts import extract_message, filter_units_by_ids, answer_views
from utils.callback_data import show_statistics

__all__ = ('register_handlers',)

from views import RestaurantCookingTimeStatisticsView


async def on_show_restaurant_cooking_time_report(
        message_or_callback_query: Message | CallbackQuery,
        state: FSMContext,
        database_api_http_client_factory: HTTPClientFactory,
        auth_api_http_client_factory: HTTPClientFactory,
        country_code: CountryCode,
) -> None:

    message = extract_message(message_or_callback_query)

    report_message = await message.answer('Загрузка...')

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
            chat_id=message_or_callback_query.from_user.id,
        )

        units = UnitsConverter(filter_units_by_ids(units, enabled_unit_ids))

    async with auth_api_http_client_factory() as http_client:

        auth_api_service = AuthAPIService(http_client)
        accounts_cookies = await get_cookies_batch(
            auth_api_service=auth_api_service,
            account_names=units.office_manager_account_names,
        )

    async with httpx.AsyncClient(timeout=30) as http_client:

        units_statistics = await get_units_kitchen_operational_statistics(
            country_code=country_code,
            accounts_cookies=accounts_cookies,
            units=units,
            http_client=http_client,
        )

    units_statistics = [
        calculate_restaurant_average_pending_and_cooking_time(
            unit_id_to_name=units.unit_id_to_name,
            report=report,
        ) for report in units_statistics
    ]
    view = RestaurantCookingTimeStatisticsView(units_statistics)
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_show_restaurant_cooking_time_report,
        Command('restaurant_cooking_time'),
    )
    dispatcher.register_callback_query_handler(
        on_show_restaurant_cooking_time_report,
        show_statistics.filter(report_type_name='RESTAURANT_COOKING_TIME'),
    )
