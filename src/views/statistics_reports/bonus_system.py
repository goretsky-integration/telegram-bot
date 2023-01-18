from typing import Iterable

import models.report_views.bonus_system as models
from views.base import BaseView

__all__ = ('BonusSystemStatisticsView',)


class BonusSystemStatisticsView(BaseView):
    __slots__ = ('__units',)

    def __init__(self, units_bonus_system_statistics: Iterable[models.UnitBonusSystemStatisticsViewDTO]):
        self.__units = sorted(units_bonus_system_statistics,
                              key=lambda unit: unit.orders_with_phone_numbers_percent,
                              reverse=True)

    def get_text(self) -> str:
        lines = ['<b>Бонусная система</b>']
        lines += [f'{unit.unit_name} | {unit.orders_with_phone_numbers_percent}% из 100' for unit in self.__units]
        return '\n'.join(lines)
