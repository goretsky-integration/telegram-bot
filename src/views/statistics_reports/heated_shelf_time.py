from typing import Iterable

import models.report_views.heated_shelf_time as models
from services.text_utils import humanize_seconds
from views.base import BaseView

__all__ = ('HeatedShelfTimeStatisticsView',)


class HeatedShelfTimeStatisticsView(BaseView):
    __slots__ = ('__units_statistics',)

    def __init__(self, heated_shelf_time_statistics: Iterable[models.UnitHeatedShelfTimeStatisticsViewDTO]):
        self.__units = sorted(heated_shelf_time_statistics,
                              reverse=True,
                              key=lambda unit_statistics: unit_statistics.average_heated_shelf_time_in_seconds)

    def get_text(self) -> str:
        lines = ['<b>Время ожидания на полке</b>']
        lines += [
            f'{unit_statistics.unit_name}'
            f' | {humanize_seconds(unit_statistics.average_heated_shelf_time_in_seconds)}'
            f' | {unit_statistics.trips_with_one_order_percentage:g}%'
            for unit_statistics in self.__units_statistics
        ]
        return '\n'.join(lines)
