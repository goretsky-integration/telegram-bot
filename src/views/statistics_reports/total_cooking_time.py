from dodolib import models

from services.text_utils import humanize_seconds
from views.base import BaseView

__all__ = ('TotalCookingTimeStatisticsView',)


class TotalCookingTimeStatisticsView(BaseView):
    __slots__ = ('__kitchen_partial_statistics', '__unit_id_to_name')

    def __init__(self, kitchen_partial_statistics: models.KitchenPartialStatisticsReport,
                 unit_id_to_name: dict[int, str]):
        self.__kitchen_partial_statistics = kitchen_partial_statistics
        self.__unit_id_to_name = unit_id_to_name

    def get_text(self) -> str:
        lines = ['<b>Общее время приготовления</b>']
        sorted_units_statistics = sorted(self.__kitchen_partial_statistics.results,
                                         key=lambda unit: unit.total_cooking_time)

        for unit in sorted_units_statistics:
            unit_name = self.__unit_id_to_name[unit.unit_id]
            lines.append(f'{unit_name} | {humanize_seconds(unit.total_cooking_time)}')

        return '\n'.join(lines)
