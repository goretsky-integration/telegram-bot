from dodolib import models

from views.base import BaseView

__all__ = ('AwaitingOrdersStatisticsView',)


class AwaitingOrdersStatisticsView(BaseView):
    __slots__ = ('__unit_id_to_name', '__delivery_partial_statistics')

    def __init__(self, delivery_partial_statistics: models.DeliveryPartialStatisticsReport,
                 unit_id_to_name: dict[int, str]):
        self.__delivery_partial_statistics = delivery_partial_statistics
        self.__unit_id_to_name = unit_id_to_name

    def get_text(self) -> str:
        lines = ['<b>Остывают на полке - В очереди (Всего)</b>']
        sorted_units_statistics = sorted(
            self.__delivery_partial_statistics.results,
            key=lambda unit: (unit.heated_shelf_orders_count, unit.couriers_in_queue_count,
                              unit.couriers_on_shift_count),
            reverse=True,
        )

        for unit in sorted_units_statistics:
            unit_name = self.__unit_id_to_name[unit.unit_id]
            lines.append(f'{unit_name} | {unit.heated_shelf_orders_count} - {unit.couriers_in_queue_count}'
                         f' ({unit.couriers_on_shift_count})')

        for unit_id in self.__delivery_partial_statistics.errors:
            unit_name = self.__unit_id_to_name[unit_id]
            lines.append(f'{unit_name} | Ошибка')

        return '\n'.join(lines)
