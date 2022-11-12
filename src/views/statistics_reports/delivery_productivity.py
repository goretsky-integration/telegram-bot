import uuid
from typing import Iterable

from dodolib import models

from services.text_utils import humanize_percents
from views.base import BaseView

__all__ = ('DeliveryProductivityStatisticsView',)


class DeliveryProductivityStatisticsView(BaseView):
    __slots__ = ('__units_delivery_productivity_statistics', '__unit_uuid_to_name')

    def __init__(self, units_delivery_productivity_statistics: Iterable[models.UnitDeliveryProductivityStatistics],
                 unit_uuid_to_name: dict[uuid.UUID, str]):
        self.__units_delivery_productivity_statistics = units_delivery_productivity_statistics
        self.__unit_uuid_to_name = unit_uuid_to_name

    def get_text(self) -> str:
        lines = ['<b>Заказов на курьера в час</b>']
        units_sorted_statistics = sorted(self.__units_delivery_productivity_statistics,
                                         key=lambda unit: unit.orders_per_courier_labour_hour_today,
                                         reverse=True)

        for unit in units_sorted_statistics:
            unit_name = self.__unit_uuid_to_name[unit.unit_uuid]
            lines.append(f'{unit_name} | {unit.orders_per_courier_labour_hour_today}'
                         f' | {humanize_percents(unit.from_week_before_in_percents)}')

        return '\n'.join(lines)
