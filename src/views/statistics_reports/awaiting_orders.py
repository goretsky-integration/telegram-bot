import models.report_views.awaiting_orders as models
from views.base import BaseView

__all__ = ('AwaitingOrdersStatisticsView',)


class AwaitingOrdersStatisticsView(BaseView):
    __slots__ = ('__unit_id_to_name', '__delivery_partial_statistics')

    def __init__(self, awaiting_orders_statistics: models.AwaitingOrdersStatisticsReportViewDTO):
        self.__error_unit_names = awaiting_orders_statistics.error_unit_names
        self.__units = sorted(
            awaiting_orders_statistics.units,
            reverse=True,
            key=lambda unit: (unit.heated_shelf_orders_count,
                              unit.couriers_in_queue_count,
                              unit.couriers_on_shift_count),
        )

    def get_text(self) -> str:
        lines = ['<b>Остывают на полке - В очереди (Всего)</b>']
        lines += [
            f'{unit.unit_name} | {unit.heated_shelf_orders_count}'
            f' - {unit.couriers_in_queue_count} ({unit.couriers_on_shift_count})'
            for unit in self.__units
        ]
        lines += [f'{unit_name} | Ошибка' for unit_name in self.__error_unit_names]
        return '\n'.join(lines)
