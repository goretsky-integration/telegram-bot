import uuid
from typing import Iterable

from dodolib import models

from services.text_utils import humanize_seconds
from views.base import BaseView

__all__ = ('RestaurantCookingTimeStatisticsView',)


class RestaurantCookingTimeStatisticsView(BaseView):
    __slots__ = ('__units_restaurant_cooking_time_statistics', '__unit_uuid_to_name')

    def __init__(self, units_restaurant_cooking_time_statistics: Iterable[models.UnitRestaurantCookingTimeStatistics],
                 unit_uuid_to_name: dict[uuid.UUID, str]):
        self.__units_restaurant_cooking_time_statistics = units_restaurant_cooking_time_statistics
        self.__unit_uuid_to_name = unit_uuid_to_name

    def get_text(self) -> str:
        lines = ['<b>Время приготовления в ресторане</b>']
        sorted_units_statistics = sorted(self.__units_restaurant_cooking_time_statistics,
                                         key=lambda unit: unit.average_tracking_pending_and_cooking_time)

        for unit in sorted_units_statistics:
            unit_name = self.__unit_uuid_to_name[unit.unit_uuid]
            lines.append(f'{unit_name} | {humanize_seconds(unit.average_tracking_pending_and_cooking_time)}')

        return '\n'.join(lines)
