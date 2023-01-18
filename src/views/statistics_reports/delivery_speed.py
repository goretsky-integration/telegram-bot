from typing import Iterable

import models.report_views.delivery_speed as models
from services.text_utils import humanize_seconds, abbreviate_unit_name
from views.base import BaseView

__all__ = ('DeliverySpeedStatisticsView',)


class DeliverySpeedStatisticsView(BaseView):
    __slots__ = ('__units_delivery_speed_statistics', '__unit_uuid_to_name')

    def __init__(self, units_delivery_speed_statistics: Iterable[models.UnitDeliverySpeedStatisticsDTO]):
        self.__units = sorted(units_delivery_speed_statistics,
                              key=lambda unit: unit.average_delivery_order_fulfillment_time)

    def get_text(self) -> str:
        lines = ['<b>Общая скорость доставки - Время приготовления - Время на полке - Поездка курьера</b>']
        lines += [
            f'{abbreviate_unit_name(unit.unit_name)}'
            f' | {humanize_seconds(unit.average_delivery_order_fulfillment_time)}'
            f' | {humanize_seconds(unit.average_cooking_time)}'
            f' | {humanize_seconds(unit.average_heated_shelf_time)}'
            f' | {humanize_seconds(unit.average_order_trip_time)}'
            for unit in self.__units
        ]
        return '\n'.join(lines)
