import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Command
from dodolib import models, AuthClient, DodoAPIClient, DatabaseClient
from dodolib.utils.convert_models import UnitsConverter

from models import Query
from shortcuts import get_message, validate_reports, answer_views, flatten
from utils import logger
from utils.callback_data import show_statistics
from views import BonusSystemStatisticsView

__all__ = ('register_handlers',)


async def on_bonus_system_statistics_report(
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
    tasks = (auth_client.get_cookies(account_name) for account_name in units.account_names)
    accounts_cookies = await asyncio.gather(*tasks)
    account_name_to_unit_id_and_name = units.account_names_to_unit_ids_and_names
    tasks = (
        api_client.get_bonus_system_statistics(
            account_cookies.cookies,
            account_name_to_unit_id_and_name[account_cookies.account_name],
        ) for account_cookies in accounts_cookies
    )
    units_statistics: tuple[list[models.UnitBonusSystem], ...] = await asyncio.gather(*tasks)
    view = BonusSystemStatisticsView(flatten(units_statistics), units.ids_to_names)
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher):
    dispatcher.register_message_handler(
        on_bonus_system_statistics_report,
        Command('bonus_system'),
    )
    dispatcher.register_callback_query_handler(
        on_bonus_system_statistics_report,
        show_statistics.filter(report_type_name='BONUS_SYSTEM'),
    )
