from typing import Iterable

import models.report_views.productivity_balance as models
from services.text_utils import humanize_seconds, intgaps
from views.base import BaseView

__all__ = ('ProductivityBalanceStatisticsView',)


class ProductivityBalanceStatisticsView(BaseView):
    __slots__ = ('__units_productivity_statistics', '__unit_uuid_to_name')

    def __init__(self, productivity_balance_statistics: Iterable[models.UnitProductivityBalanceStatisticsViewDTO]):
        self.__units = sorted(productivity_balance_statistics,
                              reverse=True,
                              key=lambda unit: unit.sales_per_labor_hour)

    def get_text(self) -> str:
        lines = ['<b>Баланс эффективности</b>']
        lines += [
            f'{unit.unit_name} | {intgaps(unit.sales_per_labor_hour)} | {unit.orders_per_labor_hour}'
            f' | {humanize_seconds(unit.stop_sale_duration_in_seconds)}'
            for unit in self.__units
        ]
        return '\n'.join(lines)
