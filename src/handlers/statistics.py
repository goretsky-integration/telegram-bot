from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery

import models.database
import responses
from bot import dp
from services import filters, api, statistics
from utils import callback_data as cd
from utils.convert_models import UnitsConverter, to_heated_shelf_orders_and_couriers_statistics


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.DAILY_REVENUE.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_daily_revenue_statistics_query(callback_query: CallbackQuery, units: UnitsConverter):
    revenue_statistics = await api.get_revenue_statistics(units.ids)
    response = responses.RevenueStatistics(revenue_statistics, units.id_to_name)
    await callback_query.message.answer(**response.as_dict())


@dp.message_handler(
    Command(models.StatisticsReportType.DAILY_REVENUE.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_daily_revenue_statistics_command(message: Message, units: UnitsConverter):
    revenue_statistics = await api.get_revenue_statistics(units.ids)
    response = responses.RevenueStatistics(revenue_statistics, units.id_to_name)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.KITCHEN_PERFORMANCE.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_update_kitchen_performance_query(callback_query: CallbackQuery, units: UnitsConverter):
    kitchen_statistics = await statistics.get_kitchen_performance_statistics(units.account_names_to_unit_ids)
    response = responses.KitchenPerformanceStatistics(kitchen_statistics, units.id_to_name)
    await callback_query.message.answer(**response.as_dict())


@dp.message_handler(
    Command(models.StatisticsReportType.KITCHEN_PERFORMANCE.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_kitchen_performance_command(message: Message, units: UnitsConverter):
    kitchen_statistics = await statistics.get_kitchen_performance_statistics(units.account_names_to_unit_ids)
    response = responses.KitchenPerformanceStatistics(kitchen_statistics, units.id_to_name)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.DELIVERY_SPEED.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_delivery_speed_query(callback_query: CallbackQuery, units: UnitsConverter):
    units_delivery_statistics = await statistics.get_delivery_speed_statistics(units.account_names_to_unit_uuids)
    response = responses.DeliverySpeedStatistics(units_delivery_statistics)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command(models.StatisticsReportType.DELIVERY_SPEED.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_delivery_speed_command(message: Message, units: UnitsConverter):
    units_delivery_statistics = await statistics.get_delivery_speed_statistics(units.account_names_to_unit_uuids)
    response = responses.DeliverySpeedStatistics(units_delivery_statistics)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.BEING_LATE_CERTIFICATES.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_being_late_certificates_query(callback_query: CallbackQuery, units: UnitsConverter):
    units_statistics = await statistics.get_being_late_certificates_statistics(
        units.account_names_to_unit_ids_and_names)
    response = responses.BeingLateCertificatesStatistics(units_statistics)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command(models.StatisticsReportType.BEING_LATE_CERTIFICATES.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_being_late_certificates_command(message: Message, units: UnitsConverter):
    units_statistics = await statistics.get_being_late_certificates_statistics(
        units.account_names_to_unit_ids_and_names)
    response = responses.BeingLateCertificatesStatistics(units_statistics)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.COOKING_TIME.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_cooking_time_query(callback_query: CallbackQuery, units: UnitsConverter):
    units_statistics = await statistics.get_kitchen_production_statistics(units.account_names_to_unit_ids)
    response = responses.CookingTimeStatistics(units_statistics, units.id_to_name)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command(models.StatisticsReportType.COOKING_TIME.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_cooking_time_command(message: Message, units: UnitsConverter):
    units_statistics = await statistics.get_kitchen_production_statistics(units.account_names_to_unit_ids)
    response = responses.CookingTimeStatistics(units_statistics, units.id_to_name)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.DELIVERY_PERFORMANCE.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_delivery_performance_query(callback_query: CallbackQuery, units: UnitsConverter):
    units_statistics = await statistics.get_delivery_performance_statistics(units.account_names_to_unit_ids)
    response = responses.DeliveryPerformanceStatistics(units_statistics, units.id_to_name)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command(models.StatisticsReportType.DELIVERY_PERFORMANCE.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_delivery_performance_command(message: Message, units: UnitsConverter):
    units_statistics = await statistics.get_delivery_performance_statistics(units.account_names_to_unit_ids)
    response = responses.DeliveryPerformanceStatistics(units_statistics, units.id_to_name)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.DELIVERY_AWAITING_TIME.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_delivery_awaiting_time_query(callback_query: CallbackQuery, units: UnitsConverter):
    units_statistics = await statistics.get_heated_shelf_statistics(units.account_names_to_unit_ids)
    response = responses.HeatedShelfTimeStatistics(units_statistics, units.id_to_name)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command(models.StatisticsReportType.DELIVERY_AWAITING_TIME.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_delivery_awaiting_time_command(message: Message, units: UnitsConverter):
    units_statistics = await statistics.get_heated_shelf_statistics(units.account_names_to_unit_ids)
    response = responses.HeatedShelfTimeStatistics(units_statistics, units.id_to_name)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.BONUS_SYSTEM.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_bonus_system_query(callback_query: CallbackQuery, units: UnitsConverter):
    units_statistics = await statistics.get_bonus_system_statistics(units.account_names_to_unit_ids_and_names)
    response = responses.BonusSystemStatistics(units_statistics)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command(models.StatisticsReportType.BONUS_SYSTEM.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_bonus_system_command(message: Message, units: UnitsConverter):
    units_statistics = await statistics.get_bonus_system_statistics(units.account_names_to_unit_ids_and_names)
    response = responses.BonusSystemStatistics(units_statistics)
    await message.answer(**response.as_dict())


@dp.callback_query_handler(
    cd.show_statistics.filter(name=models.StatisticsReportType.AWAITING_ORDERS.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_awaiting_orders_query(callback_query: CallbackQuery, units: UnitsConverter):
    heated_shelf_statistics = await statistics.get_heated_shelf_statistics(units.account_names_to_unit_ids)
    couriers_statistics = await statistics.get_couriers_statistics(units.account_names_to_unit_ids)
    heated_shelf_orders_and_couriers_statistics = to_heated_shelf_orders_and_couriers_statistics(
        heated_shelf_statistics, couriers_statistics)
    response = responses.HeatedShelfOrdersAndCouriersStatistics(
        heated_shelf_orders_and_couriers_statistics, units.id_to_name)
    await callback_query.message.answer(**response.as_dict())
    await callback_query.answer()


@dp.message_handler(
    Command(models.StatisticsReportType.AWAITING_ORDERS.name),
    filters.UnitIdsRequiredFilter(),
)
async def on_awaiting_orders_command(message: Message, units: UnitsConverter):
    heated_shelf_statistics = await statistics.get_heated_shelf_statistics(units.account_names_to_unit_ids)
    couriers_statistics = await statistics.get_couriers_statistics(units.account_names_to_unit_ids)
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


@dp.message_handler(Command([report_type.name for report_type in models.StatisticsReportType]))
async def on_no_enabled_units_command(message: Message):
    await message.answer('Кажется вы не добавили ни одну точку продаж для отображения 😕\n'
                         'Чтобы это сделать, нажмите на кнопку ⚙️ Настройки или введите команду /settings.\n'
                         'Далее нажмите на кнопку Отчёты по статистике и отметьте точки продаж.')
