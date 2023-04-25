import models.report_views.delivery_cooking_time as models
from services.text_utils import humanize_seconds
from views.base import BaseView

__all__ = ('DeliveryCookingTimeStatisticsView',)


class DeliveryCookingTimeStatisticsView(BaseView):
    __slots__ = ('__kitchen_partial_statistics', '__unit_id_to_name')

    def __init__(self, total_cooking_time_statistics: models.DeliveryCookingTimeStatisticsReportViewDTO):
        self.__units = sorted(total_cooking_time_statistics.units, key=lambda unit: unit.total_cooking_time)
        self.__error_unit_names = total_cooking_time_statistics.error_unit_names

    def get_text(self) -> str:
        lines = ['<b>Время приготовления на доставку</b>']
        lines += [
            f'{unit.unit_name} | {humanize_seconds(unit.total_cooking_time)}'
            for unit in self.__units
        ]
        return '\n'.join(lines)
