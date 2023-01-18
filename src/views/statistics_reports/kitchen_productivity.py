import models.report_views.kitchen_productivity as models
from services.text_utils import intgaps
from views.base import BaseView

__all__ = ('KitchenProductivityStatisticsView',)


class KitchenProductivityStatisticsView(BaseView):
    __slots__ = ('__kitchen_productivity_statistics', '__unit_id_to_name')

    def __init__(self, kitchen_productivity_statistics: models.KitchenProductivityStatisticsReportViewDTO):
        self.__units = sorted(kitchen_productivity_statistics.units,
                              key=lambda unit: unit.sales_per_labor_hour_today,
                              reverse=True)
        self.__error_unit_names = kitchen_productivity_statistics.error_unit_names

    def get_text(self) -> str:
        lines = ['<b>Выручка на чел. в час</b>']
        lines += [
            f'{unit.unit_name} | {intgaps(unit.sales_per_labor_hour_today)}'
            f' | {unit.from_week_before_percent:+}%'
            for unit in self.__units
        ]
        lines += [f'{unit_name} | Ошибка' for unit_name in self.__error_unit_names]
        return '\n'.join(lines)
