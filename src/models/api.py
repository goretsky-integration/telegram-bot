import uuid
from typing import TypedDict

from pydantic import BaseModel, NonNegativeInt

__all__ = (
    'RevenueForTodayAndWeekBeforeStatistics',
    'RestaurantOrdersStatistics',
    'RevenueStatistics',
    'UnitsRevenueMetadata',
    'UnitBonusSystem',
    'UnitBeingLateCertificatesTodayAndWeekBefore',
    'UnitDeliverySpeed',
    'UnitKitchenPerformance',
    'KitchenPerformanceStatistics',
    'UnitDeliveryPerformance',
    'DeliveryPerformanceStatistics',
    'HeatedShelfStatistics',
    'UnitHeatedShelf',
    'UnitCouriers',
    'CouriersStatistics',
    'KitchenProductionStatistics',
    'UnitKitchenProduction',
    'UnitIdAndName',
    'UnitHeatedShelfOrdersAndCouriers',
    'HeatedShelfOrdersAndCouriersStatistics',
)


class UnitsRevenueMetadata(BaseModel):
    total_revenue_today: NonNegativeInt
    total_revenue_week_before: NonNegativeInt
    delta_from_week_before: float


class RevenueForTodayAndWeekBeforeStatistics(BaseModel):
    unit_id: int
    today: int
    week_before: int
    delta_from_week_before: float


class RevenueStatistics(BaseModel):
    units: list[RevenueForTodayAndWeekBeforeStatistics]
    metadata: UnitsRevenueMetadata
    error_unit_ids: list[int]


class RestaurantOrdersStatistics(BaseModel):
    department: str
    orders_with_phone_numbers_count: int
    orders_with_phone_numbers_percentage: int
    total_orders_count: int


class UnitBeingLateCertificatesTodayAndWeekBefore(BaseModel):
    unit_id: int
    unit_name: str
    certificates_today_count: int
    certificates_week_before_count: int


class UnitDeliverySpeed(BaseModel):
    unit_uuid: uuid.UUID
    unit_name: str
    average_cooking_time: int
    average_delivery_order_fulfillment_time: int
    average_heated_shelf_time: int
    average_order_trip_time: int


class UnitKitchenPerformance(BaseModel):
    unit_id: int
    revenue_per_hour: int
    revenue_delta_from_week_before: int


class KitchenPerformanceStatistics(BaseModel):
    units: list[UnitKitchenPerformance]
    error_unit_ids: list[int]


class UnitDeliveryPerformance(BaseModel):
    unit_id: int
    orders_for_courier_count_per_hour_today: float
    orders_for_courier_count_per_hour_week_before: float
    delta_from_week_before: int


class DeliveryPerformanceStatistics(BaseModel):
    units: list[UnitDeliveryPerformance]
    error_unit_ids: list[int]


class UnitHeatedShelf(BaseModel):
    unit_id: int
    average_awaiting_time: int
    awaiting_orders_count: int


class HeatedShelfStatistics(BaseModel):
    units: list[UnitHeatedShelf]
    error_unit_ids: list[int]


class UnitCouriers(BaseModel):
    unit_id: int
    in_queue_count: int
    total_count: int


class CouriersStatistics(BaseModel):
    units: list[UnitCouriers]
    error_unit_ids: list[int]


class UnitKitchenProduction(BaseModel):
    unit_id: int
    average_cooking_time: int


class KitchenProductionStatistics(BaseModel):
    units: list[UnitKitchenProduction]
    error_unit_ids: list[int]


class UnitBonusSystem(BaseModel):
    unit_name: str
    orders_with_phone_numbers_count: int
    orders_with_phone_numbers_percent: float
    total_orders_count: int


class UnitIdAndName(TypedDict):
    id: int
    name: str


class UnitHeatedShelfOrdersAndCouriers(BaseModel):
    unit_id: int
    awaiting_orders_count: int
    in_queue_count: int
    total_count: int


class HeatedShelfOrdersAndCouriersStatistics(BaseModel):
    units: list[UnitHeatedShelfOrdersAndCouriers]
    error_unit_ids: list[int]
