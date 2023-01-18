import collections
import functools
from dataclasses import dataclass
from typing import Iterable
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
    'to_late_delivery_vouchers_statistics_view_dto',
)


def to_late_delivery_vouchers_statistics_view_dto(
        units_late_delivery_vouchers_statistics: Iterable[api_models.UnitLateDeliveryVouchersStatisticsReport],
        unit_uuid_to_name: dict[UUID, str],
) -> list[view_models.UnitLateDeliveryVouchersStatisticsViewDTO]:
    return [
        view_models.UnitLateDeliveryVouchersStatisticsViewDTO(
            unit_name=unit_uuid_to_name[unit.unit_uuid],
            certificates_count_today=unit.certificates_count_today,
            certificates_count_week_before=unit.certificates_count_week_before,
        ) for unit in units_late_delivery_vouchers_statistics
    ]


def to_delivery_speed_statistics_view_dto(
        units_delivery_speed_statistics: Iterable[api_models.UnitDeliverySpeedStatisticsReport],
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
        kitchen_productivity_statistics_group: Iterable[api_models.KitchenProductivityStatisticsReport],
        unit_id_to_name: dict[int, str]
) -> view_models.KitchenProductivityStatisticsReportViewDTO:
    units = []
    error_unit_names = []
    for kitchen_productivity_statistics in kitchen_productivity_statistics_group:
        units += [
            view_models.UnitKitchenProductivityStatisticsDTO(
                unit_name=unit_id_to_name[unit.unit_id],
                total_cooking_time=unit.total_cooking_time,
                sales_per_labor_hour_today=unit.sales_per_labor_hour_today,
                from_week_before_percent=unit.from_week_before_percent,
            ) for unit in kitchen_productivity_statistics.results
        ]
        error_unit_names += [unit_id_to_name[unit_id] for unit_id in kitchen_productivity_statistics.errors]
    return view_models.KitchenProductivityStatisticsReportViewDTO(
        units=units,
        error_unit_names=error_unit_names,
    )


def to_awaiting_orders_statistics_view_dto(
        awaiting_orders_statistics_group: Iterable[api_models.AwaitingOrdersStatisticsReport],
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
        error_unit_names += [unit_id_to_name[unit_id] for unit_id in awaiting_orders_statistics.errors]
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
        error_unit_names=[unit_id_to_name[unit_id] for unit_id in revenue_statistics.errors]
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
    def uuids(self) -> set[UUID]:
        return {unit.uuid for unit in self.units}

    @functools.cached_property
    def account_names(self) -> set[str]:
        return {unit.account_name for unit in self.units}

    @functools.cached_property
    def unit_id_to_name(self) -> dict[int, str]:
        return {unit.id: unit.name for unit in self.units}

    @functools.cached_property
    def unit_uuid_to_name(self) -> dict[UUID, str]:
        return {unit.uuid: unit.name for unit in self.units}

    @functools.cached_property
    def grouped_by_account_name(self) -> dict[str, 'UnitsConverter']:
        account_name_to_units = collections.defaultdict(list)
        for unit in self.units:
            account_name_to_units[unit.account_name].append(unit)
        return {account_name: UnitsConverter(units) for account_name, units in account_name_to_units.items()}
