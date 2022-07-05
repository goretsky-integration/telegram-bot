from pydantic import BaseModel, NonNegativeInt, PositiveInt

__all__ = (
    'UnitRevenueForTodayAndWeekBefore',
    'UnitsRevenueMetadata',
    'UnitsRevenueStatistics',
    'KitchenStatistics',
    'Tracking',
    'ProductSpending',
    'KitchenStatisticsBatch',
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


class KitchenRevenue(BaseModel):
    per_hour: NonNegativeInt
    delta_from_week_before: float


class ProductSpending(BaseModel):
    per_hour: NonNegativeInt
    delta_from_week_before: float


class Tracking(BaseModel):
    postponed: NonNegativeInt
    in_queue: NonNegativeInt
    in_work: NonNegativeInt


class KitchenStatistics(BaseModel):
    unit_id: PositiveInt
    revenue: KitchenRevenue
    product_spending: ProductSpending
    average_cooking_time: NonNegativeInt
    tracking: Tracking


class KitchenStatisticsBatch(BaseModel):
    kitchen_statistics: list[KitchenStatistics]
    error_unit_ids: list[PositiveInt]
