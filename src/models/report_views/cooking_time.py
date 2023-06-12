from dataclasses import dataclass

__all__ = ('UnitCookingTimeStatisticsViewDTO',)


@dataclass(frozen=True, slots=True)
class UnitCookingTimeStatisticsViewDTO:
    unit_name: str
    average_tracking_pending_and_cooking_time: int
