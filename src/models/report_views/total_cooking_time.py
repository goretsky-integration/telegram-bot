from dataclasses import dataclass
from typing import Iterable

__all__ = ('UnitTotalCookingTimeStatisticsDTO', 'TotalCookingTimeStatisticsReportViewDTO')


@dataclass(frozen=True, slots=True)
class UnitTotalCookingTimeStatisticsDTO:
    unit_name: str
    total_cooking_time: 0


@dataclass(frozen=True, slots=True)
class TotalCookingTimeStatisticsReportViewDTO:
    units: Iterable[UnitTotalCookingTimeStatisticsDTO]
    error_unit_names: Iterable[str]
