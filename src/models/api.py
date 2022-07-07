import uuid

from pydantic import BaseModel, NonNegativeInt, PositiveInt, NonNegativeFloat

__all__ = (
    'UnitRevenueForTodayAndWeekBefore',
    'UnitsRevenueMetadata',
    'UnitsRevenueStatistics',
    'KitchenStatistics',
    'Tracking',
    'ProductSpending',
    'KitchenStatisticsBatch',
    'UnitDeliveryStatistics',
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


class UnitDeliveryStatistics(BaseModel):
    unit_id: uuid.UUID
    unit_name: str
    average_cooking_time: NonNegativeInt
    average_delivery_order_fulfillment_time: NonNegativeInt
    average_heated_shelf_time: NonNegativeInt
    average_order_trip_time: NonNegativeInt
    couriers_shifts_duration: NonNegativeInt
    delivery_orders_count: NonNegativeInt
    delivery_sales: NonNegativeInt
    late_orders_count: NonNegativeInt
    orders_with_courier_app_count: NonNegativeInt
    trips_count: NonNegativeInt
    trips_duration: NonNegativeInt
    orders_for_courier_count_per_hour: NonNegativeFloat
    delivery_with_courier_app_percent: NonNegativeFloat
    couriers_workload: NonNegativeFloat
