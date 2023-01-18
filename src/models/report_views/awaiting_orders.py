from dataclasses import dataclass
from typing import Iterable

__all__ = ('UnitAwaitingOrdersStatisticsDTO', 'AwaitingOrdersStatisticsReportViewDTO')


@dataclass(frozen=True, slots=True)
class UnitAwaitingOrdersStatisticsDTO:
    unit_name: str
    heated_shelf_orders_count: int
    couriers_in_queue_count: int
    couriers_on_shift_count: int


@dataclass(frozen=True, slots=True)
class AwaitingOrdersStatisticsReportViewDTO:
    units: Iterable[UnitAwaitingOrdersStatisticsDTO]
    error_unit_names: Iterable[str]
