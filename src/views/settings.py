from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup

import models.api_responses.database as models

from keyboards import UnitsMarkup, RegionsMarkup
from views.base import BaseView

__all__ = (
    'RegionsResponseView',
    'UnitsResponseView',
)


class RegionsResponseView(BaseView):

    def __init__(self, report_type_id: int, regions: Iterable[models.Region]):
        self.__regions = regions
        self.__report_type_id = report_type_id

    def get_text(self) -> str:
        return 'Выберите регион подразделений'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return RegionsMarkup(self.__report_type_id, self.__regions)


class UnitsResponseView(BaseView):

    def __init__(self, report_type_id: int, region_id: int,
                 enabled_unit_ids: Iterable[int],
                 all_units: Iterable[models.Unit]):
        self.__report_type_id = report_type_id
        self.__enabled_unit_ids = enabled_unit_ids
        self.__all_units = all_units
        self.__region_id = region_id

    def get_text(self) -> str:
        return 'Выберите точки продаж для отслеживания'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return UnitsMarkup(
            report_type_id=self.__report_type_id,
            region_id=self.__region_id,
            enabled_unit_ids=self.__enabled_unit_ids,
            all_units=self.__all_units,
        )
