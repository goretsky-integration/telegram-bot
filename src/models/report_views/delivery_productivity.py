from dataclasses import dataclass

__all__ = ('UnitDeliveryProductivityStatisticsViewDTO',)


@dataclass(frozen=True, slots=True)
class UnitDeliveryProductivityStatisticsViewDTO:
    unit_name: str
    orders_per_courier_labour_hour_today: float
    from_week_before_in_percents: int
