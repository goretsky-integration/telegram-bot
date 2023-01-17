import models.report_views.revenue as models
from services.text_utils import intgaps
from views.base import BaseView

__all__ = ('RevenueStatisticsView',)


class RevenueStatisticsView(BaseView):
    __slots__ = ('__units', '__total')

    def __init__(self, revenue_statistics: models.RevenueStatisticsReportViewDTO):
        self.__total = revenue_statistics.total
        self.__units = sorted(revenue_statistics.units, reverse=True,
                              key=lambda unit_statistics: unit_statistics.revenue_today)

    def get_text(self) -> str:
        lines = ['<b>Выручка за сегодня</b>']
        lines += [
            f'{unit.unit_name}'
            f' | {intgaps(unit.revenue_today)}'
            f' | {unit.from_week_before_in_percents:+}%'
            for unit in self.__units
        ]
        lines.append(f'<b>Итого: {intgaps(self.__total.revenue_today)}'
                     f' | {self.__total.from_week_before_in_percents:+}%</b>')
        return '\n'.join(lines)
