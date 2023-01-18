from typing import Iterable

import models.report_views.delivery_productivity as models
from views.base import BaseView

__all__ = ('DeliveryProductivityStatisticsView',)


class DeliveryProductivityStatisticsView(BaseView):
    __slots__ = ('__units',)

    def __init__(self, delivery_productivity_statistics: Iterable[models.UnitDeliveryProductivityStatisticsViewDTO]):
        self.__units = sorted(delivery_productivity_statistics,
                              key=lambda unit: unit.orders_per_courier_labour_hour_today,
                              reverse=True)

    def get_text(self) -> str:
        lines = ['<b>Заказов на курьера в час</b>']
        lines += [
            f'{unit.unit_name} | {unit.orders_per_courier_labour_hour_today}'
            f' | {unit.from_week_before_in_percents:+}%'
            for unit in self.__units
        ]
        return '\n'.join(lines)
