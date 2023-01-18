from dataclasses import dataclass

__all__ = ('UnitRestaurantCookingTimeStatisticsViewDTO',)


@dataclass(frozen=True, slots=True)
class UnitRestaurantCookingTimeStatisticsViewDTO:
    unit_name: str
    average_tracking_pending_and_cooking_time: int
