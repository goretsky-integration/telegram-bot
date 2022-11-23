from typing import Iterable

from aiogram.types import InlineKeyboardMarkup
from dodolib import models

from keyboards import UnitsMarkup, RegionsMarkup
from views.base import BaseView

__all__ = (
    'RegionsResponseView',
    'UnitsResponseView',
)


class RegionsResponseView(BaseView):

    def __init__(self, report_type: str, regions: Iterable[str]):
        self.__regions = regions
        self.__report_type = report_type

    def get_text(self) -> str:
        return 'Выберите регион подразделений'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return RegionsMarkup(self.__report_type, self.__regions)


class UnitsResponseView(BaseView):

    def __init__(self, report_type: str, region: str,
                 enabled_unit_ids: Iterable[int], all_units: Iterable[models.Unit]):
        self.__report_type = report_type
        self.__enabled_unit_ids = enabled_unit_ids
        self.__all_units = all_units
        self.__region = region

    def get_text(self) -> str:
        return 'Выберите точки продаж для отслеживания'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return UnitsMarkup(self.__report_type, self.__region, self.__enabled_unit_ids, self.__all_units)
