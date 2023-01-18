from uuid import UUID

from pydantic import BaseModel

__all__ = ('UnitDeliverySpeedStatisticsReport',)


class UnitDeliverySpeedStatisticsReport(BaseModel):
    unit_uuid: UUID
    average_cooking_time: int
    average_delivery_order_fulfillment_time: int
    average_heated_shelf_time: int
    average_order_trip_time: int
