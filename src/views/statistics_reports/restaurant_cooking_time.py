from typing import Iterable

import models.report_views.restaurant_cooking_time as models
from services.text_utils import humanize_seconds
from views.base import BaseView

__all__ = ('RestaurantCookingTimeStatisticsView',)


class RestaurantCookingTimeStatisticsView(BaseView):
    __slots__ = ('__units',)

    def __init__(self, restaurant_cooking_time_statistics: Iterable[models.UnitRestaurantCookingTimeStatisticsViewDTO]):
        self.__units = sorted(restaurant_cooking_time_statistics,
                              key=lambda unit: unit.average_tracking_pending_and_cooking_time)

    def get_text(self) -> str:
        lines = ['<b>Время приготовления в ресторане</b>']
        lines += [
            f'{unit.unit_name} | {humanize_seconds(unit.average_tracking_pending_and_cooking_time)}'
            for unit in self.__units
        ]
        return '\n'.join(lines)
