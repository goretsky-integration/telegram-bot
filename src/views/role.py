from collections.abc import Iterable

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

import models.api_responses
from views.base import BaseView

__all__ = ('RoleMenuView',)


class RoleMenuView(BaseView):
    reply_markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton('Сменить роль', callback_data='set_role'),
            ]
        ]
    )

    def __init__(
            self,
            *,
            region_units: Iterable[models.RegionUnits],
            report_types: Iterable[models.api_responses.ReportType],
    ):
        self.__region_units = region_units
        self.__report_types = report_types

    def get_text(self) -> str:
        lines: list[str] = ['<b>Ваши доступы:</b>']

        lines.append('\n🏠 <b>Точки продаж:</b>')
        for region_unit in self.__region_units:
            lines.append(f'\n📍 <b>{region_unit.region.name}</b>')

            for unit in region_unit.units:
                lines.append(unit.name)

        lines.append('\n\n📱 <b>Отчёты:</b>')
        for report_type in self.__report_types:
            lines.append(report_type.verbose_name)
        return '\n'.join(lines)
