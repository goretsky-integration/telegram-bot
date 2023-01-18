from dataclasses import dataclass

__all__ = ('UnitBonusSystemStatisticsViewDTO',)


@dataclass(frozen=True, slots=True)
class UnitBonusSystemStatisticsViewDTO:
    unit_name: str
    orders_with_phone_numbers_percent: float
