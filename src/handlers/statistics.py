import asyncio

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from dodolib import DodoAPIClient, AuthClient

import models
import responses
from bot import dp
from services import filters
from services.batch_operations import (
    get_cookies_batch,
    get_tokens_batch,
    get_statistics_batch_by_unit_ids,
    get_statistics_batch_by_unit_uuids,
    get_statistics_batch_by_unit_ids_and_names,
)
from services.strategies import STATISTICS_REPORT_TYPE_TO_STRATEGY
from utils import callback_data as cd
from utils import constants
from utils.convert_models import UnitsConverter, to_heated_shelf_orders_and_couriers_statistics


@dp.callback_query_handler(
    cd.show_statistics.filter(report_type_name=constants.StatisticsReportType.DAILY_REVENUE.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_daily_revenue_statistics_query(
        callback_query: CallbackQuery,
        units: UnitsConverter,
        dodo_client: DodoAPIClient,
):
    revenue_statistics = await dodo_client.get_revenue_statistics(units.ids)
    response = responses.RevenueStatistics(revenue_statistics, units.id_to_name)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command(constants.StatisticsReportType.DAILY_REVENUE.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_daily_revenue_statistics_command(
        message: Message,
        units: UnitsConverter,
        dodo_client: DodoAPIClient,
):
    revenue_statistics = await dodo_client.get_revenue_statistics(units.ids)
    response = responses.RevenueStatistics(revenue_statistics, units.id_to_name)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(report_type_name=[
        constants.StatisticsReportType.KITCHEN_PERFORMANCE.name,
        constants.StatisticsReportType.DELIVERY_PERFORMANCE.name,
        constants.StatisticsReportType.COOKING_TIME.name,
        constants.StatisticsReportType.DELIVERY_AWAITING_TIME.name,
    ]),
    filters.UnitIdsRequiredFilter(),
)
async def on_update_kitchen_performance_query(
        callback_query: CallbackQuery,
        units: UnitsConverter,
        dodo_client: DodoAPIClient,
        auth_client: AuthClient,
        callback_data: dict,
):
    strategy = STATISTICS_REPORT_TYPE_TO_STRATEGY[callback_data['report_type_name']]
    accounts_cookies = await get_cookies_batch(auth_client, units.account_names)
    response_statistics = await get_statistics_batch_by_unit_ids(
        dodo_client_method=strategy['method'],
        dodo_client=dodo_client,
        accounts_cookies=accounts_cookies,
        account_names_to_unit_ids=units.account_names_to_unit_ids,
        response_model=strategy['model'],
    )
    response = strategy['response'](response_statistics, units.id_to_name)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command([
        constants.StatisticsReportType.KITCHEN_PERFORMANCE.name,
        constants.StatisticsReportType.DELIVERY_PERFORMANCE.name,
        constants.StatisticsReportType.COOKING_TIME.name,
        constants.StatisticsReportType.DELIVERY_AWAITING_TIME.name,
    ]),
    filters.UnitIdsRequiredFilter(),
)
async def on_kitchen_performance_command(
        message: Message,
        units: UnitsConverter,
        dodo_client: DodoAPIClient,
        auth_client: AuthClient,
        command: Command
):
    strategy = STATISTICS_REPORT_TYPE_TO_STRATEGY[command.command.upper()]
    accounts_cookies = await get_cookies_batch(auth_client, units.account_names)
    response_statistics = await get_statistics_batch_by_unit_ids(
        dodo_client_method=strategy['method'],
        dodo_client=dodo_client,
        accounts_cookies=accounts_cookies,
        account_names_to_unit_ids=units.account_names_to_unit_ids,
        response_model=strategy['model'],
    )
    response = strategy['response'](response_statistics, units.id_to_name)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(report_type_name=[
        constants.StatisticsReportType.DELIVERY_SPEED.name,
        constants.StatisticsReportType.RESTAURANT_COOKING_TIME.name,
    ]),
    filters.UnitIdsRequiredFilter(),
)
async def on_delivery_speed_query(
        callback_query: CallbackQuery,
        units: UnitsConverter,
        auth_client: AuthClient,
        dodo_client: DodoAPIClient,
        callback_data: dict,
):
    strategy = STATISTICS_REPORT_TYPE_TO_STRATEGY[callback_data['report_type_name']]
    tokens = await get_tokens_batch(auth_client, units.account_names)
    response_statistics = await get_statistics_batch_by_unit_uuids(
        dodo_client_method=strategy['method'],
        dodo_client=dodo_client,
        account_tokens=tokens,
        account_names_to_unit_uuids=units.account_names_to_unit_uuids,
        response_model=strategy['model']
    )
    response = strategy['response'](response_statistics, units.uuids_to_names)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command([
        constants.StatisticsReportType.DELIVERY_SPEED.name,
        constants.StatisticsReportType.RESTAURANT_COOKING_TIME.name,
    ]),
    filters.UnitIdsRequiredFilter(),
)
async def on_delivery_speed_command(
        message: Message,
        units: UnitsConverter,
        auth_client: AuthClient,
        dodo_client: DodoAPIClient,
        command: Command,
):
    strategy = STATISTICS_REPORT_TYPE_TO_STRATEGY[command.command.upper()]
    tokens = await get_tokens_batch(auth_client, units.account_names)
    response_statistics = await get_statistics_batch_by_unit_uuids(
        dodo_client_method=strategy['method'],
        dodo_client=dodo_client,
        account_tokens=tokens,
        account_names_to_unit_uuids=units.account_names_to_unit_uuids,
        response_model=strategy['model']
    )
    response = strategy['response'](response_statistics, units.uuids_to_names)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(report_type_name=[
        constants.StatisticsReportType.BEING_LATE_CERTIFICATES.name,
        constants.StatisticsReportType.BONUS_SYSTEM.name,
    ]),
    filters.UnitIdsRequiredFilter(),
)
async def on_being_late_certificates_query(
        callback_query: CallbackQuery,
        units: UnitsConverter,
        auth_client: AuthClient,
        dodo_client: DodoAPIClient,
        callback_data: dict,
):
    strategy = STATISTICS_REPORT_TYPE_TO_STRATEGY[callback_data['report_type_name']]
    accounts_cookies = await get_cookies_batch(auth_client, units.account_names)
    response_statistics = await get_statistics_batch_by_unit_ids_and_names(
        dodo_client_method=strategy['method'],
        dodo_client=dodo_client,
        accounts_cookies=accounts_cookies,
        account_names_to_unit_ids_and_names=units.account_names_to_unit_ids_and_names,
        response_model=strategy['model'],
    )
    response = strategy['response'](response_statistics)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command([
        constants.StatisticsReportType.BEING_LATE_CERTIFICATES.name,
        constants.StatisticsReportType.BONUS_SYSTEM.name,
    ]),
    filters.UnitIdsRequiredFilter(),
)
async def on_being_late_certificates_command(
        message: Message,
        units: UnitsConverter,
        auth_client: AuthClient,
        dodo_client: DodoAPIClient,
        command: Command,
):
    strategy = STATISTICS_REPORT_TYPE_TO_STRATEGY[command.command.upper()]
    accounts_cookies = await get_cookies_batch(auth_client, units.account_names)
    response_statistics = await get_statistics_batch_by_unit_ids_and_names(
        dodo_client_method=strategy['method'],
        dodo_client=dodo_client,
        accounts_cookies=accounts_cookies,
        account_names_to_unit_ids_and_names=units.account_names_to_unit_ids_and_names,
        response_model=strategy['model'],
    )
    response = strategy['response'](response_statistics)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(report_type_name=constants.StatisticsReportType.AWAITING_ORDERS.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_awaiting_orders_query(
        callback_query: CallbackQuery,
        units: UnitsConverter,
        auth_client: AuthClient,
        dodo_client: DodoAPIClient,
):
    accounts_cookies = await get_cookies_batch(auth_client, units.account_names)
    task1 = get_statistics_batch_by_unit_ids(
        dodo_client_method=DodoAPIClient.get_heated_shelf_time_statistics,
        dodo_client=dodo_client,
        accounts_cookies=accounts_cookies,
        account_names_to_unit_ids=units.account_names_to_unit_ids,
        response_model=models.HeatedShelfStatistics,
    )
    task2 = get_statistics_batch_by_unit_ids(
        dodo_client_method=DodoAPIClient.get_couriers_statistics,
        dodo_client=dodo_client,
        accounts_cookies=accounts_cookies,
        account_names_to_unit_ids=units.account_names_to_unit_ids,
        response_model=models.CouriersStatistics,
    )
    heated_shelf_statistics, couriers_statistics = await asyncio.gather(task1, task2)
    heated_shelf_orders_and_couriers_statistics = to_heated_shelf_orders_and_couriers_statistics(
        heated_shelf_statistics, couriers_statistics)
    response = responses.HeatedShelfOrdersAndCouriersStatistics(
        heated_shelf_orders_and_couriers_statistics, units.id_to_name)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command(constants.StatisticsReportType.AWAITING_ORDERS.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_awaiting_orders_command(
        message: Message,
        units: UnitsConverter,
        auth_client: AuthClient,
        dodo_client: DodoAPIClient,
):
    accounts_cookies = await get_cookies_batch(auth_client, units.account_names)
    task1 = get_statistics_batch_by_unit_ids(
        dodo_client_method=DodoAPIClient.get_heated_shelf_time_statistics,
        dodo_client=dodo_client,
        accounts_cookies=accounts_cookies,
        account_names_to_unit_ids=units.account_names_to_unit_ids,
        response_model=models.HeatedShelfStatistics,
    )
    task2 = get_statistics_batch_by_unit_ids(
        dodo_client_method=DodoAPIClient.get_couriers_statistics,
        dodo_client=dodo_client,
        accounts_cookies=accounts_cookies,
        account_names_to_unit_ids=units.account_names_to_unit_ids,
        response_model=models.CouriersStatistics,
    )
    heated_shelf_statistics, couriers_statistics = await asyncio.gather(task1, task2)
    heated_shelf_orders_and_couriers_statistics = to_heated_shelf_orders_and_couriers_statistics(
        heated_shelf_statistics, couriers_statistics)
    response = responses.HeatedShelfOrdersAndCouriersStatistics(
        heated_shelf_orders_and_couriers_statistics, units.id_to_name)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(cd.show_statistics.filter())
async def on_no_enabled_units_query(callback_query: CallbackQuery):
    await callback_query.message.answer(
        'Кажется вы не добавили ни одну точку продаж для отображения 😕\n'
        'Чтобы это сделать, нажмите на кнопку ⚙️ Настройки или введите команду /settings.\n'
        'Далее нажмите на кнопку Отчёты по статистике и отметьте точки продаж.')
    await callback_query.answer()


@dp.message_handler(Command([report_type.name for report_type in constants.StatisticsReportType]))
async def on_no_enabled_units_command(message: Message):
    await message.answer('Кажется вы не добавили ни одну точку продаж для отображения 😕\n'
                         'Чтобы это сделать, нажмите на кнопку ⚙️ Настройки или введите команду /settings.\n'
                         'Далее нажмите на кнопку Отчёты по статистике и отметьте точки продаж.')
