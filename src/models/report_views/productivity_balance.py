from dataclasses import dataclass

__all__ = ('UnitProductivityBalanceStatisticsViewDTO',)


@dataclass(frozen=True, slots=True)
class UnitProductivityBalanceStatisticsViewDTO:
    unit_name: str
    sales_per_labor_hour: int
    orders_per_labor_hour: int
    stop_sale_duration_in_seconds: int
