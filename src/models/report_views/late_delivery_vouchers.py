from dataclasses import dataclass

__all__ = ('UnitLateDeliveryVouchersStatisticsViewDTO',)


@dataclass(frozen=True, slots=True)
class UnitLateDeliveryVouchersStatisticsViewDTO:
    unit_name: str
    certificates_count_today: int
    certificates_count_week_before: int
