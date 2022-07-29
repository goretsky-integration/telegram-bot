"""
Cookies and unit ids based models.


Cookies, unit ids and unit names based models.
- UnitBeingLateCertificatesTodayAndWeekBefore
- UnitBonusSystem

Tokens and unit UUIDs based models.
- UnitDeliverySpeed
- UnitOrdersHandoverTime

"""

import uuid
from enum import Enum

from pydantic import BaseModel, NonNegativeInt

from models.type_aliases import UnitIdAndName

__all__ = (
    'RevenueForTodayAndWeekBeforeStatistics',
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
    'UnitHeatedShelfOrdersAndCouriers',
    'HeatedShelfOrdersAndCouriersStatistics',
    'UnitOrdersHandoverTime',
    'SalesChannel',
    'OrdersHandoverTimeStatistics',
    'DeliverySpeedStatistics',
    'BonusSystemStatistics',
    'BeingLateCertificatesStatistics',
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


class UnitHeatedShelfOrdersAndCouriers(BaseModel):
    unit_id: int
    awaiting_orders_count: int
    in_queue_count: int
    total_count: int


class HeatedShelfOrdersAndCouriersStatistics(BaseModel):
    units: list[UnitHeatedShelfOrdersAndCouriers]
    error_unit_ids: list[int]


# Models by cookies, unit ids and unit names


class UnitBeingLateCertificatesTodayAndWeekBefore(BaseModel):
    unit_id: int
    unit_name: str
    certificates_today_count: int
    certificates_week_before_count: int


class BeingLateCertificatesStatistics(BaseModel):
    units: list[UnitBeingLateCertificatesTodayAndWeekBefore]
    error_unit_ids_and_names: list[UnitIdAndName]


class UnitBonusSystem(BaseModel):
    unit_name: str
    orders_with_phone_numbers_count: int
    orders_with_phone_numbers_percent: float
    total_orders_count: int


class BonusSystemStatistics(BaseModel):
    units: list[UnitBonusSystem]
    error_unit_ids_and_names: list[UnitIdAndName]


# Models by tokens and unit UUIDs


class SalesChannel(Enum):
    DINE_IN = 'Dine-in'
    TAKEAWAY = 'Takeaway'
    DELIVERY = 'Delivery'


class UnitOrdersHandoverTime(BaseModel):
    unit_uuid: uuid.UUID
    unit_name: str
    average_tracking_pending_time: int
    average_cooking_time: int
    average_heated_shelf_time: int
    sales_channels: list[SalesChannel]


class OrdersHandoverTimeStatistics(BaseModel):
    units: list[UnitOrdersHandoverTime]
    error_unit_uuids: list[uuid.UUID]


class UnitDeliverySpeed(BaseModel):
    unit_uuid: uuid.UUID
    unit_name: str
    average_cooking_time: int
    average_delivery_order_fulfillment_time: int
    average_heated_shelf_time: int
    average_order_trip_time: int


class DeliverySpeedStatistics(BaseModel):
    units: list[UnitDeliverySpeed]
    error_unit_uuids: list[uuid.UUID]
