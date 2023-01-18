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
    def grouped_by_account_name(self) -> dict[str, 'UnitsConverter']:
        account_name_to_units = collections.defaultdict(list)
        for unit in self.units:
            account_name_to_units[unit.account_name].append(unit)
        return {account_name: UnitsConverter(units) for account_name, units in account_name_to_units.items()}
