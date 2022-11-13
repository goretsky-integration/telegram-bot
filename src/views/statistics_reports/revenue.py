from dodolib.models import RevenueStatistics

from services.text_utils import intgaps, humanize_percents
from views.base import BaseView

__all__ = ('RevenueStatisticsView',)


class RevenueStatisticsView(BaseView):
    __slots__ = ('__revenue_statistics', '__unit_id_to_name')

    def __init__(self, revenue_statistics: RevenueStatistics, unit_id_to_name: dict[int, str]):
        self.__revenue_statistics = revenue_statistics
        self.__unit_id_to_name = unit_id_to_name

    def get_text(self) -> str:
        lines = ['<b>Выручка за сегодня</b>']
        units_revenue = sorted(self.__revenue_statistics.results.units, reverse=True,
                               key=lambda unit_revenue: unit_revenue.today)

        for unit_revenue in units_revenue:
            unit_name = self.__unit_id_to_name[unit_revenue.unit_id]
            lines.append(f'{unit_name} | {intgaps(unit_revenue.today)}'
                         f' | {humanize_percents(unit_revenue.from_week_before_in_percents)}')

        lines.append(f'<b>Итого: {intgaps(self.__revenue_statistics.results.total.today)}'
                     f' | {humanize_percents(self.__revenue_statistics.results.total.from_week_before_in_percents)}</b>')

        return '\n'.join(lines)
