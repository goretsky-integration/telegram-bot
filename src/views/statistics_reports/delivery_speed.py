import uuid
from typing import Iterable

from dodolib import models

from services.text_utils import abbreviate_unit_name, humanize_seconds
from views.base import BaseView

__all__ = ('DeliverySpeedStatisticsView',)


class DeliverySpeedStatisticsView(BaseView):
    __slots__ = ('__units_delivery_speed_statistics', '__unit_uuid_to_name')

    def __init__(self, units_delivery_speed_statistics: Iterable[models.UnitDeliverySpeed],
                 unit_uuid_to_name: dict[uuid.UUID, str]):
        self.__units_delivery_speed_statistics = units_delivery_speed_statistics
        self.__unit_uuid_to_name = unit_uuid_to_name

    def get_text(self) -> str:
        lines = ['<b>Общая скорость доставки - Время приготовления - Время на полке - Поездка курьера</b>']
        units_sorted_statistics = sorted(self.__units_delivery_speed_statistics,
                                         key=lambda unit: unit.average_delivery_order_fulfillment_time)

        for unit in units_sorted_statistics:
            unit_name = abbreviate_unit_name(self.__unit_uuid_to_name[unit.unit_uuid])
            order_fulfillment_time = humanize_seconds(unit.average_delivery_order_fulfillment_time)
            cooking_time = humanize_seconds(unit.average_cooking_time)
            heated_shelf_time = humanize_seconds(unit.average_heated_shelf_time)
            order_trip_time = humanize_seconds(unit.average_order_trip_time)
            lines.append(f'{unit_name}'
                         f' | {order_fulfillment_time}'
                         f' | {cooking_time}'
                         f' | {heated_shelf_time}'
                         f' | {order_trip_time}')

        return '\n'.join(lines)
