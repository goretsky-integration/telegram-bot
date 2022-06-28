from pydantic import BaseModel, NonNegativeInt, PositiveInt

__all__ = (
    'UnitRevenueForTodayAndWeekBefore',
    'UnitsRevenueMetadata',
    'UnitsRevenueStatistics',
)


class UnitRevenueForTodayAndWeekBefore(BaseModel):
    unit_id: PositiveInt
    today: NonNegativeInt
    week_before: NonNegativeInt
    delta_from_week_before: float


class UnitsRevenueMetadata(BaseModel):
    total_revenue_today: NonNegativeInt
    total_revenue_week_before: NonNegativeInt
    delta_from_week_before: float


class UnitsRevenueStatistics(BaseModel):
    revenues: list[UnitRevenueForTodayAndWeekBefore]
    metadata: UnitsRevenueMetadata
    error_unit_ids: list[int]
