from dataclasses import dataclass

__all__ = ('UnitDeliverySpeedStatisticsDTO',)


@dataclass(frozen=True, slots=True)
class UnitDeliverySpeedStatisticsDTO:
    unit_name: str
    average_delivery_order_fulfillment_time: int
    average_cooking_time: int
    average_heated_shelf_time: int
    average_order_trip_time: int
