from typing import Iterable

from dodolib import models
from views.base import BaseView

__all__ = ('BonusSystemStatisticsView',)


class BonusSystemStatisticsView(BaseView):
    __slots__ = ('__units_bonus_system_statistics', '__unit_id_to_name')

    def __init__(self, units_bonus_system_statistics: Iterable[models.UnitBonusSystem],
                 unit_id_to_name: dict[int, str]):
        self.__units_bonus_system_statistics = units_bonus_system_statistics
        self.__unit_id_to_name = unit_id_to_name

    def get_text(self) -> str:
        lines = ['<b>Бонусная система</b>']
        sorted_units_statistics = sorted(
            self.__units_bonus_system_statistics,
            key=lambda unit: unit.orders_with_phone_numbers_percent,
            reverse=True
        )

        for unit in sorted_units_statistics:
            unit_name = self.__unit_id_to_name[unit.unit_id]
            lines.append(f'{unit_name} | {unit.orders_with_phone_numbers_percent}% из 100')

        return '\n'.join(lines)
