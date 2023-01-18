from dataclasses import dataclass
from typing import Iterable

__all__ = ('UnitKitchenProductivityStatisticsDTO', 'KitchenProductivityStatisticsReportViewDTO')


@dataclass(frozen=True, slots=True)
class UnitKitchenProductivityStatisticsDTO:
    unit_name: str
    sales_per_labor_hour_today: 0
    from_week_before_percent: 0


@dataclass(frozen=True, slots=True)
class KitchenProductivityStatisticsReportViewDTO:
    units: Iterable[UnitKitchenProductivityStatisticsDTO]
    error_unit_names: Iterable[str]
