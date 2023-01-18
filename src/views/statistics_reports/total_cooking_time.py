import models.report_views.total_cooking_time as models
from services.text_utils import humanize_seconds
from views.base import BaseView

__all__ = ('TotalCookingTimeStatisticsView',)


class TotalCookingTimeStatisticsView(BaseView):
    __slots__ = ('__kitchen_partial_statistics', '__unit_id_to_name')

    def __init__(self, total_cooking_time_statistics: models.TotalCookingTimeStatisticsReportViewDTO):
        self.__units = sorted(total_cooking_time_statistics.units, key=lambda unit: unit.total_cooking_time)
        self.__error_unit_names = total_cooking_time_statistics.error_unit_names

    def get_text(self) -> str:
        lines = ['<b>Общее время приготовления</b>']
        lines += [
            f'{unit.unit_name} | {humanize_seconds(unit.total_cooking_time)}'
            for unit in self.__units
        ]
        return '\n'.join(lines)
