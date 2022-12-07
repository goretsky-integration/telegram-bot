import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from dodolib import DatabaseClient, AuthClient, DodoAPIClient
from dodolib.utils.convert_models import UnitsConverter

from models import Query
from shortcuts import answer_views, validate_reports, get_message, flatten, filter_units_by_ids, filter_exceptions
from utils import logger
from utils.callback_data import show_statistics
from views import RestaurantCookingTimeStatisticsView


async def on_restaurant_cooking_time_statistics_report(
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
    tasks = (auth_client.get_tokens(account_name) for account_name in units.account_names)
    accounts_tokens = await asyncio.gather(*tasks)
    account_name_to_unit_uuids = units.account_names_to_unit_uuids
    tasks = (api_client.get_restaurant_cooking_time_statistics(account_tokens.access_token, 'ru',
                                                               account_name_to_unit_uuids[account_tokens.account_name])
             for account_tokens in accounts_tokens)
    units_statistics = await asyncio.gather(*tasks, return_exceptions=True)
    units_statistics = filter_exceptions(units_statistics)
    view = RestaurantCookingTimeStatisticsView(flatten(units_statistics), units.uuid_to_name())
    await answer_views(report_message, view, edit=True)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_restaurant_cooking_time_statistics_report,
        Command('restaurant_cooking_time'),
    )
    dispatcher.register_callback_query_handler(
        on_restaurant_cooking_time_statistics_report,
        show_statistics.filter(report_type_name='RESTAURANT_COOKING_TIME'),
    )
