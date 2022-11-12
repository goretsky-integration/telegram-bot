import uuid
from typing import Iterable

from dodolib import models

from services.text_utils import humanize_seconds
from views.base import BaseView

__all__ = ('HeatedShelfTimeStatisticsView',)


class HeatedShelfTimeStatisticsView(BaseView):
    __slots__ = ('__units_heated_shelf_time_statistics', '__unit_uuid_to_name')

    def __init__(self, units_heated_shelf_time_statistics: Iterable[models.UnitHeatedShelfStatistics],
                 unit_uuid_to_name: dict[uuid.UUID, str]):
        self.__units_heated_shelf_time_statistics = units_heated_shelf_time_statistics
        self.__unit_uuid_to_name = unit_uuid_to_name

    def get_text(self) -> str:
        lines = ['<b>Время ожидания на полке</b>']
        sorted_units_statistics = sorted(self.__units_heated_shelf_time_statistics,
                                         reverse=True,
                                         key=lambda unit: unit.average_heated_shelf_time)

        for unit in sorted_units_statistics:
            unit_name = self.__unit_uuid_to_name[unit.unit_uuid]
            lines.append(f'{unit_name} | {humanize_seconds(unit.average_heated_shelf_time)}')

        return '\n'.join(lines)
