from pydantic import BaseModel

__all__ = (
    'UnitRevenueStatistics',
    'UnitsRevenueStatistics',
    'RevenueStatisticsReport',
    'TotalRevenueStatistics',
)


class UnitRevenueStatistics(BaseModel):
    unit_id: int
    today: int
    from_week_before_in_percents: int


class TotalRevenueStatistics(BaseModel):
    today: int
    from_week_before_in_percents: int


class UnitsRevenueStatistics(BaseModel):
    units: list[UnitRevenueStatistics]
    total: TotalRevenueStatistics


class RevenueStatisticsReport(BaseModel):
    results: UnitsRevenueStatistics
    errors: set[int]
