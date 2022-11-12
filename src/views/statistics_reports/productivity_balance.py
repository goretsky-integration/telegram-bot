import uuid
from typing import Iterable

import models
from services.text_utils import humanize_seconds, intgaps
from views.base import BaseView

__all__ = ('ProductivityBalanceStatisticsView',)


class ProductivityBalanceStatisticsView(BaseView):
    __slots__ = ('__units_productivity_statistics', '__unit_uuid_to_name')

    def __init__(self, units_productivity_statistics: Iterable[models.UnitProductivityBalanceStatistics],
                 unit_uuid_to_name: dict[uuid.UUID, str]):
        self.__units_productivity_statistics = units_productivity_statistics
        self.__unit_uuid_to_name = unit_uuid_to_name

    def get_text(self) -> str:
        lines = ['<b>Баланс эффективности</b>']
        sorted_units_productivity_statistics = sorted(self.__units_productivity_statistics,
                                                      reverse=True,
                                                      key=lambda unit: unit.sales_per_labor_hour)

        for unit in sorted_units_productivity_statistics:
            unit_name = self.__unit_uuid_to_name[unit.unit_uuid]
            lines.append(f'{unit_name} | {intgaps(unit.sales_per_labor_hour)} | {unit.orders_per_labor_hour}'
                         f' | {humanize_seconds(unit.stop_sale_duration_in_seconds)}')

        return '\n'.join(lines)
