from collections.abc import Iterable
from typing import TypeAlias

from models.report_views.cooking_time import UnitCookingTimeStatisticsViewDTO
from services.text_utils import humanize_seconds
from views.base import BaseView

__all__ = (
    'RestaurantCookingTimeStatisticsView',
    'DeliveryCookingTimeStatisticsView',
)

UnitsCookingTimeStatistics: TypeAlias = (
    Iterable[UnitCookingTimeStatisticsViewDTO]
)


class CookingTimeStatisticsView(BaseView):

    __slots__ = ('__units',)

    title = '<b>Время приготовления</b>'

    def __init__(
            self,
            units_cooking_time_statistics: UnitsCookingTimeStatistics,
    ):
        self.__units = sorted(
            units_cooking_time_statistics,
            key=lambda unit: unit.average_tracking_pending_and_cooking_time
        )

    def get_text(self) -> str:
        lines = [self.title]
        lines += [
            f'{unit.unit_name} | {humanize_seconds(unit.average_tracking_pending_and_cooking_time)}'
            for unit in self.__units
        ]
        return '\n'.join(lines)


class RestaurantCookingTimeStatisticsView(CookingTimeStatisticsView):
    title = '<b>Время приготовления в ресторане</b>'


class DeliveryCookingTimeStatisticsView(CookingTimeStatisticsView):
    title = '<b>Время приготовления на доставку</b>'
