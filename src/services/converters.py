import collections
import functools
from dataclasses import dataclass
from typing import Iterable, Self, Mapping, TypeAlias
from uuid import UUID


import models.api_responses.database as database_models
import models.api_responses.dodo as api_models
import models.report_views as view_models

__all__ = (
    'to_revenue_statistics_view_dto',
    'UnitsConverter',
    'to_awaiting_orders_statistics_view_dto',
    'to_kitchen_productivity_statistics_view_dto',
    'to_delivery_speed_statistics_view_dto',
    'to_restaurant_cooking_time_statistics_view_dto',
    'to_productivity_balance_statistics_view_dto',
    'to_delivery_productivity_statistics_view_dto',
    'to_delivery_cooking_time_statistics_view_dto',
    'to_heated_shelf_time_statistics_view_dto',
    'to_bonus_system_statistics_view_dto',
)



def to_bonus_system_statistics_view_dto(
        bonus_system_statistics: Iterable[
            api_models.UnitBonusSystemStatisticsReport],
        unit_id_to_name: dict[int, str],
) -> list[view_models.UnitBonusSystemStatisticsViewDTO]:
    return [
        view_models.UnitBonusSystemStatisticsViewDTO(
            unit_name=unit_id_to_name[unit.unit_id],
            orders_with_phone_numbers_percent=unit.orders_with_phone_numbers_percent,
        ) for unit in bonus_system_statistics
    ]


def to_heated_shelf_time_statistics_view_dto(
        heated_shelf_time_statistics: Iterable[
            api_models.UnitHeatedShelfTimeStatisticsReport],
        unit_uuid_to_trips_with_one_order_percentage: Mapping[UUID, int],
        unit_uuid_to_name: Mapping[UUID, str],
) -> list[view_models.UnitHeatedShelfTimeStatisticsViewDTO]:
    return [
        view_models.UnitHeatedShelfTimeStatisticsViewDTO(
            unit_name=unit_uuid_to_name[unit.unit_uuid],
            average_heated_shelf_time_in_seconds=unit.average_heated_shelf_time,
            trips_with_one_order_percentage=(
                unit_uuid_to_trips_with_one_order_percentage
                .get(unit.unit_uuid, 0)
            ),
        ) for unit in heated_shelf_time_statistics
    ]


def to_delivery_cooking_time_statistics_view_dto(
        kitchen_productivity_statistics_group: Iterable[
            api_models.KitchenProductivityStatisticsReport],
        unit_id_to_name: dict[int, str]
) -> view_models.DeliveryCookingTimeStatisticsReportViewDTO:
    units = []
    error_unit_names = []
    for kitchen_productivity_statistics in kitchen_productivity_statistics_group:
        units += [
            view_models.UnitDeliveryCookingTimeStatisticsDTO(
                unit_name=unit_id_to_name[unit.unit_id],
                total_cooking_time=unit.total_cooking_time,
            ) for unit in kitchen_productivity_statistics.results
        ]
        error_unit_names += [unit_id_to_name[unit_id] for unit_id in
                             kitchen_productivity_statistics.errors]
    return view_models.DeliveryCookingTimeStatisticsReportViewDTO(units=units,
                                                                  error_unit_names=error_unit_names)


def to_delivery_productivity_statistics_view_dto(
        units_delivery_productivity_statistics: Iterable[
            api_models.UnitDeliveryProductivityStatisticsReport],
        unit_uuid_to_name: dict[UUID, str],
) -> list[view_models.UnitDeliveryProductivityStatisticsViewDTO]:
    return [
        view_models.UnitDeliveryProductivityStatisticsViewDTO(
            unit_name=unit_uuid_to_name[unit.unit_uuid],
            orders_per_courier_labour_hour_today=unit.orders_per_courier_labour_hour_today,
            from_week_before_in_percents=unit.from_week_before_in_percents,
        ) for unit in units_delivery_productivity_statistics
    ]


def to_productivity_balance_statistics_view_dto(
        units_productivity_balance_statistics: Iterable[
            api_models.UnitProductivityBalanceStatisticsReport],
        unit_uuid_to_name: dict[UUID, str],
) -> list[view_models.UnitProductivityBalanceStatisticsViewDTO]:
    return [
        view_models.UnitProductivityBalanceStatisticsViewDTO(
            unit_name=unit_uuid_to_name[unit.unit_uuid],
            stop_sale_duration_in_seconds=unit.stop_sale_duration_in_seconds,
            sales_per_labor_hour=unit.sales_per_labor_hour,
            orders_per_labor_hour=unit.orders_per_labor_hour,
        ) for unit in units_productivity_balance_statistics
    ]


def to_restaurant_cooking_time_statistics_view_dto(
        units_restaurant_cooking_time_statistics: Iterable[
            api_models.UnitRestaurantCookingTimeStatisticsReport],
        unit_uuid_to_name: dict[UUID, str],
) -> list[view_models.UnitRestaurantCookingTimeStatisticsViewDTO]:
    return [
        view_models.UnitRestaurantCookingTimeStatisticsViewDTO(
            unit_name=unit_uuid_to_name[unit.unit_uuid],
            average_tracking_pending_and_cooking_time=unit.average_tracking_pending_and_cooking_time,
        ) for unit in units_restaurant_cooking_time_statistics
    ]


def to_delivery_speed_statistics_view_dto(
        units_delivery_speed_statistics: Iterable[
            api_models.UnitDeliverySpeedStatisticsReport],
        unit_uuid_to_name: dict[UUID, str],
) -> list[view_models.UnitDeliverySpeedStatisticsDTO]:
    return [
        view_models.UnitDeliverySpeedStatisticsDTO(
            unit_name=unit_uuid_to_name[unit.unit_uuid],
            average_delivery_order_fulfillment_time=unit.average_delivery_order_fulfillment_time,
            average_cooking_time=unit.average_cooking_time,
            average_order_trip_time=unit.average_order_trip_time,
            average_heated_shelf_time=unit.average_heated_shelf_time,
        ) for unit in units_delivery_speed_statistics
    ]


def to_kitchen_productivity_statistics_view_dto(
        kitchen_productivity_statistics_group: Iterable[
            api_models.KitchenProductivityStatisticsReport],
        unit_id_to_name: dict[int, str]
) -> view_models.KitchenProductivityStatisticsReportViewDTO:
    units = []
    error_unit_names = []
    for kitchen_productivity_statistics in kitchen_productivity_statistics_group:
        units += [
            view_models.UnitKitchenProductivityStatisticsDTO(
                unit_name=unit_id_to_name[unit.unit_id],
                sales_per_labor_hour_today=unit.sales_per_labor_hour_today,
                from_week_before_percent=unit.from_week_before_percent,
            ) for unit in kitchen_productivity_statistics.results
        ]
        error_unit_names += [unit_id_to_name[unit_id] for unit_id in
                             kitchen_productivity_statistics.errors]
    return view_models.KitchenProductivityStatisticsReportViewDTO(
        units=units,
        error_unit_names=error_unit_names,
    )


def to_awaiting_orders_statistics_view_dto(
        awaiting_orders_statistics_group: Iterable[
            api_models.AwaitingOrdersStatisticsReport],
        unit_id_to_name: dict[int, str],
) -> view_models.AwaitingOrdersStatisticsReportViewDTO:
    units = []
    error_unit_names = []
    for awaiting_orders_statistics in awaiting_orders_statistics_group:
        units += [
            view_models.UnitAwaitingOrdersStatisticsDTO(
                unit_name=unit_id_to_name[unit.unit_id],
                heated_shelf_orders_count=unit.heated_shelf_orders_count,
                couriers_in_queue_count=unit.couriers_in_queue_count,
                couriers_on_shift_count=unit.couriers_on_shift_count,
            ) for unit in awaiting_orders_statistics.results
        ]
        error_unit_names += [unit_id_to_name[unit_id] for unit_id in
                             awaiting_orders_statistics.errors]
    return view_models.AwaitingOrdersStatisticsReportViewDTO(
        units=units,
        error_unit_names=error_unit_names,
    )


def to_revenue_statistics_view_dto(
        revenue_statistics: api_models.RevenueStatisticsReport,
        unit_id_to_name: dict[int, str],
) -> view_models.RevenueStatisticsReportViewDTO:
    return view_models.RevenueStatisticsReportViewDTO(
        units=[
            view_models.UnitRevenueStatisticsDTO(
                unit_name=unit_id_to_name[unit.unit_id],
                revenue_today=unit.today,
                from_week_before_in_percents=unit.from_week_before_in_percents,
            ) for unit in revenue_statistics.results.units
        ],
        total=view_models.TotalRevenueStatisticsDTO(
            revenue_today=revenue_statistics.results.total.today,
            from_week_before_in_percents=revenue_statistics.results.total.from_week_before_in_percents,
        ),
        error_unit_names=[unit_id_to_name[unit_id] for unit_id in
                          revenue_statistics.errors]
    )


@dataclass
class UnitsConverter:
    units: Iterable[database_models.Unit]

    @functools.cached_property
    def ids(self) -> set[int]:
        return {unit.id for unit in self.units}

    @functools.cached_property
    def names(self) -> set[str]:
        return {unit.name for unit in self.units}

    @functools.cached_property
    def ids_and_names(self) -> list[dict]:
        return [{'id': unit.id, 'name': unit.name} for unit in self.units]

    @functools.cached_property
    def uuids(self) -> set[UUID]:
        return {unit.uuid for unit in self.units}

    @functools.cached_property
    def office_manager_account_names(self) -> set[str]:
        return {unit.office_manager_account_name for unit in self.units}

    @functools.cached_property
    def dodo_is_api_account_names(self) -> set[str]:
        return {unit.dodo_is_api_account_name for unit in self.units}

    @functools.cached_property
    def unit_id_to_name(self) -> dict[int, str]:
        return {unit.id: unit.name for unit in self.units}

    @functools.cached_property
    def unit_uuid_to_name(self) -> dict[UUID, str]:
        return {unit.uuid: unit.name for unit in self.units}

    @functools.cached_property
    def grouped_by_office_manager_account_name(self) -> dict[str, Self]:
        account_name_to_units = collections.defaultdict(list)
        for unit in self.units:
            account_name_to_units[unit.office_manager_account_name].append(unit)
        return {
            account_name: UnitsConverter(units)
            for account_name, units in account_name_to_units.items()
        }

    @functools.cached_property
    def grouped_by_dodo_is_api_account_name(self) -> dict[str, Self]:
        account_name_to_units = collections.defaultdict(list)
        for unit in self.units:
            account_name_to_units[unit.dodo_is_api_account_name].append(unit)
        return {
            account_name: UnitsConverter(units)
            for account_name, units in account_name_to_units.items()
        }
