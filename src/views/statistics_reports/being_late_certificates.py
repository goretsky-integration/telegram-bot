import uuid
from typing import Iterable

from dodolib import models

from views.base import BaseView

__all__ = ('BeingLateCertificatesStatisticsView',)


class BeingLateCertificatesStatisticsView(BaseView):
    __slots__ = ('____units_being_late_certificates_statistics', '__unit_uuid_to_name',)

    def __init__(self, units_being_late_certificates_statistics: Iterable[models.UnitBeingLateCertificates],
                 unit_uuid_to_name: dict[uuid.UUID, str]):
        self.__units_being_late_certificates_statistics = units_being_late_certificates_statistics
        self.__unit_uuid_to_name = unit_uuid_to_name

    def get_text(self) -> str:
        lines = ['<b>Сертификаты за опоздание (сегодня) | (неделю назад)</b>']
        sorted_units_statistics = sorted(
            self.__units_being_late_certificates_statistics,
            key=lambda unit: (unit.certificates_count_today, unit.certificates_count_week_before),
            reverse=True,
        )

        for unit in sorted_units_statistics:
            unit_name = self.__unit_uuid_to_name[unit.unit_uuid]
            lines.append(f'{unit_name} | {unit.certificates_count_today} шт | {unit.certificates_count_week_before} шт')

        return '\n'.join(lines)
