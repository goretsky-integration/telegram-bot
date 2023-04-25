from dataclasses import dataclass
from typing import Iterable

__all__ = ('UnitDeliveryCookingTimeStatisticsDTO',
           'DeliveryCookingTimeStatisticsReportViewDTO')


@dataclass(frozen=True, slots=True)
class UnitDeliveryCookingTimeStatisticsDTO:
    unit_name: str
    total_cooking_time: 0


@dataclass(frozen=True, slots=True)
class DeliveryCookingTimeStatisticsReportViewDTO:
    units: Iterable[UnitDeliveryCookingTimeStatisticsDTO]
    error_unit_names: Iterable[str]

