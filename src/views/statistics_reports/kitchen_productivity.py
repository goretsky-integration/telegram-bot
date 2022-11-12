from dodolib import models

from services.text_utils import intgaps, humanize_percents
from views.base import BaseView

__all__ = ('KitchenProductivityStatisticsView',)


class KitchenProductivityStatisticsView(BaseView):
    __slots__ = ('__kitchen_productivity_statistics', '__unit_id_to_name')

    def __init__(self, kitchen_productivity_statistics: models.KitchenPartialStatisticsReport,
                 unit_id_to_name: dict[int, str]):
        self.__kitchen_productivity_statistics = kitchen_productivity_statistics
        self.__unit_id_to_name = unit_id_to_name

    def get_text(self) -> str:
        lines = ['<b>Выручка на чел. в час</b>']
        sorted_units_statistics = sorted(self.__kitchen_productivity_statistics.results,
                                         reverse=True,
                                         key=lambda unit: unit.sales_per_labor_hour_today)

        for unit in sorted_units_statistics:
            unit_name = self.__unit_id_to_name[unit.unit_id]
            lines.append(f'{unit_name} | {intgaps(unit.sales_per_labor_hour_today)}'
                         f' | {humanize_percents(unit.from_week_before_percent)}')

        return '\n'.join(lines)
