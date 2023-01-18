from dataclasses import dataclass

__all__ = ('UnitHeatedShelfTimeStatisticsViewDTO',)


@dataclass(frozen=True, slots=True)
class UnitHeatedShelfTimeStatisticsViewDTO:
    unit_name: str
    average_heated_shelf_time_in_seconds: int
    trips_with_one_order_percentage: float
