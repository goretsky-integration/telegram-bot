from typing import Iterable

import keyboards
import models
from responses.base import Response, ReplyMarkup

__all__ = (
    'RegionsResponse',
    'UnitsResponse',
)


class RegionsResponse(Response):

    def __init__(self, report_type: str, regions: Iterable[models.Region]):
        self.__regions = regions
        self.__report_type = report_type

    def get_text(self) -> str:
        return 'Выберите регион подразделений'

    def get_reply_markup(self) -> ReplyMarkup:
        return keyboards.RegionsMarkup(self.__report_type, self.__regions)


class UnitsResponse(Response):

    def __init__(self, report_type: str, region_id: int,
                 enabled_unit_ids: Iterable[int], all_units: Iterable[models.Unit]):
        self.__report_type = report_type
        self.__enabled_unit_ids = enabled_unit_ids
        self.__all_units = all_units
        self.__region_id = region_id

    def get_text(self) -> str:
        return 'Выберите точки продаж для отслеживания'

    def get_reply_markup(self) -> ReplyMarkup:
        return keyboards.UnitsMarkup(self.__report_type, self.__region_id, self.__enabled_unit_ids, self.__all_units)
