import uuid
from typing import Iterable

import models.report_views.late_delivery_vouchers as models
from views.base import BaseView

__all__ = ('BeingLateCertificatesStatisticsView',)


class BeingLateCertificatesStatisticsView(BaseView):
    __slots__ = ('____units_being_late_certificates_statistics', '__unit_uuid_to_name',)

    def __init__(self, being_late_certificates_statistics: Iterable[models.UnitLateDeliveryVouchersStatisticsViewDTO]):
        self.__units = sorted(
            being_late_certificates_statistics,
            key=lambda unit: (unit.certificates_count_today, unit.certificates_count_week_before),
            reverse=True,
        )

    def get_text(self) -> str:
        lines = ['<b>Сертификаты за опоздание (сегодня) | (неделю назад)</b>']
        lines += [
            f'{unit.unit_name} | {unit.certificates_count_today} шт | {unit.certificates_count_week_before} шт'
            for unit in self.__units
        ]
        return '\n'.join(lines)
