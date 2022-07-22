from typing import Iterable

import models
from responses.base import Response
from services.text_utils import humanize_percents, intgaps, humanize_seconds, abbreviate_unit_name


class RevenueStatistics(Response):

    def __init__(self, revenue_statistics: models.RevenueStatistics, unit_id_to_name: dict[int, str]):
        self.__units_statistics = revenue_statistics.units
        self.__error_unit_ids = revenue_statistics.error_unit_ids
        self.__metadata = revenue_statistics.metadata
        self.__unit_id_to_name = unit_id_to_name

    def get_text(self) -> str | None:
        revenues = sorted(self.__units_statistics, reverse=True, key=lambda report: report.today)
        lines = ['<b>Выручка за сегодня:</b>']

        for revenue in revenues:
            unit_name = self.__unit_id_to_name[revenue.unit_id]
            revenue_today = intgaps(revenue.today)
            delta_from_week_before = humanize_percents(round(revenue.delta_from_week_before))
            lines.append(f'{unit_name} | {revenue_today} | {delta_from_week_before}')

        for unit_id in self.__error_unit_ids:
            unit_name = self.__unit_id_to_name[unit_id]
            lines.append(f'{unit_name} | Ошибка...')

        total_revenue_today = intgaps(self.__metadata.total_revenue_today)
        delta_from_week_before = humanize_percents(round(self.__metadata.delta_from_week_before))
        lines.append(f'<b>Итого: {total_revenue_today} | {delta_from_week_before}</b>')

        return '\n'.join(lines)


class KitchenPerformanceStatistics(Response):

    def __init__(self, kitchen_statistics: models.KitchenPerformanceStatistics, unit_id_to_name: dict[int, str]):
        self.__units_statistics = kitchen_statistics.units
        self.__error_unit_ids = kitchen_statistics.error_unit_ids
        self.__unit_id_to_name = unit_id_to_name

    def get_sorted_units_statistics(self) -> list[models.UnitKitchenPerformance]:
        return sorted(self.__units_statistics, key=lambda unit: unit.revenue_per_hour, reverse=True)

    def get_text(self) -> str:
        lines = ['<b>Выручка на чел. в час</b>']
        for unit in self.get_sorted_units_statistics():
            unit_name = self.__unit_id_to_name[unit.unit_id]
            revenue_per_hour = intgaps(unit.revenue_per_hour)
            delta_from_week_before = humanize_percents(round(unit.revenue_delta_from_week_before))
            lines.append(f'{unit_name} | {revenue_per_hour} | {delta_from_week_before}')

        for error_unit_id in self.__error_unit_ids:
            unit_name = self.__unit_id_to_name[error_unit_id]
            lines.append(f'{unit_name} | <b>Ошибка</b>')

        return '\n'.join(lines)


class DeliverySpeedStatistics(Response):

    def __init__(self, units_delivery_statistics: Iterable[models.UnitDeliverySpeed]):
        self.__units_statistics = units_delivery_statistics

    def get_sorted_units_statistics(self) -> list[models.UnitDeliverySpeed]:
        return sorted(self.__units_statistics, key=lambda unit: unit.average_delivery_order_fulfillment_time)

    def get_text(self) -> str:
        lines = ['<b>Общая скорость доставки - Время приготовления - Время на полке - Поездка курьера</b>']
        for unit_delivery_statistics in self.get_sorted_units_statistics():
            order_fulfillment_time = humanize_seconds(unit_delivery_statistics.average_delivery_order_fulfillment_time)
            cooking_time = humanize_seconds(unit_delivery_statistics.average_cooking_time)
            heated_shelf_time = humanize_seconds(unit_delivery_statistics.average_heated_shelf_time)
            order_trip_time = humanize_seconds(unit_delivery_statistics.average_order_trip_time)
            unit_name = abbreviate_unit_name(unit_delivery_statistics.unit_name)
            lines.append(f'{unit_name}'
                         f' | {order_fulfillment_time}'
                         f' | {cooking_time}'
                         f' | {heated_shelf_time}'
                         f' | {order_trip_time}')
        return '\n'.join(lines)


class BeingLateCertificatesStatistics(Response):

    def __init__(self, units_being_late_certificates: Iterable[models.UnitBeingLateCertificatesTodayAndWeekBefore]):
        self.__units_statistics = units_being_late_certificates

    def get_sorted_units_statistics(self) -> list[models.UnitBeingLateCertificatesTodayAndWeekBefore]:
        return sorted(self.__units_statistics, reverse=True,
                      key=lambda unit: (unit.certificates_today_count, unit.certificates_week_before_count))

    def get_text(self) -> str:
        lines = ['<b>Сертификаты за опоздание (сегодня) | (неделю назад)</b>']
        for report in self.get_sorted_units_statistics():
            lines.append(f'{report.unit_name}'
                         f' | {report.certificates_today_count} шт'
                         f' | {report.certificates_week_before_count} шт')

        return '\n'.join(lines)


class CookingTimeStatistics(Response):

    def __init__(self, units_kitchen_statistics: models.KitchenProductionStatistics, unit_id_to_name: dict[int, str]):
        self.__units_statistics = units_kitchen_statistics.units
        self.__error_unit_ids = units_kitchen_statistics.error_unit_ids
        self.__unit_id_to_name = unit_id_to_name

    def get_sorted_units_statistics(self) -> list[models.UnitKitchenProduction]:
        return sorted(self.__units_statistics, key=lambda unit: unit.average_cooking_time)

    def get_text(self) -> str:
        lines = ['<b>Время приготовления:</b>']
        for unit in self.get_sorted_units_statistics():
            unit_name = self.__unit_id_to_name[unit.unit_id]
            average_cooking_time = humanize_seconds(unit.average_cooking_time)
            lines.append(f'{unit_name} | {average_cooking_time}')
        return '\n'.join(lines)


class BonusSystemStatistics(Response):

    def __init__(self, units_bonus_system_statistics: Iterable[models.UnitBonusSystem]):
        self.__units_statistics = units_bonus_system_statistics

    def get_sorted_units_statistics(self) -> list[models.UnitBonusSystem]:
        return sorted(self.__units_statistics, reverse=True, key=lambda unit: unit.orders_with_phone_numbers_percent)

    def get_text(self) -> str:
        lines = ['<b>Бонусная система:</b>']
        units_statistics = self.get_sorted_units_statistics()
        for unit in units_statistics:
            orders_with_phone_numbers_percent = round(unit.orders_with_phone_numbers_percent)
            lines.append(f'{unit.unit_name} | {orders_with_phone_numbers_percent}% из 100')
        return '\n'.join(lines)


class DeliveryPerformanceStatistics(Response):

    def __init__(self, delivery_performance_statistics: models.DeliveryPerformanceStatistics,
                 unit_id_to_name: dict[int, str]):
        self.__units_statistics = delivery_performance_statistics.units
        self.__error_unit_ids = delivery_performance_statistics.error_unit_ids
        self.__unit_id_to_name = unit_id_to_name

    def get_sorted_units_statistics(self) -> list[models.UnitDeliveryPerformance]:
        return sorted(self.__units_statistics, reverse=True,
                      key=lambda unit: unit.orders_for_courier_count_per_hour_today)

    def get_text(self) -> str:
        lines = ['<b>Заказов на курьера в час:</b>']
        for unit in self.get_sorted_units_statistics():
            unit_name = self.__unit_id_to_name[unit.unit_id]
            orders_count_today = unit.orders_for_courier_count_per_hour_today
            delta_from_week_before = humanize_percents(unit.delta_from_week_before)
            lines.append(f'{unit_name} | {orders_count_today} | {delta_from_week_before}')
        return '\n'.join(lines)


class HeatedShelfTimeStatistics(Response):

    def __init__(self, heated_shelf_statistics: models.HeatedShelfStatistics, unit_id_to_name: dict[int, str]):
        self.__units_statistics = heated_shelf_statistics.units
        self.__error_unit_ids = heated_shelf_statistics.error_unit_ids
        self.__unit_id_to_name = unit_id_to_name

    def get_sorted_units_statistics(self) -> list[models.UnitHeatedShelf]:
        return sorted(self.__units_statistics, key=lambda unit: unit.average_awaiting_time, reverse=True)

    def get_text(self) -> str:
        lines = ['<b>Время ожидания на полке:</b>']
        for unit in self.get_sorted_units_statistics():
            unit_name = self.__unit_id_to_name[unit.unit_id]
            average_awaiting_time = humanize_seconds(unit.average_awaiting_time)
            lines.append(f'{unit_name} | {average_awaiting_time}')
        return '\n'.join(lines)


class HeatedShelfOrdersAndCouriersStatistics(Response):

    def __init__(self, heated_shelf_orders_and_couriers_statistics: models.HeatedShelfOrdersAndCouriersStatistics,
                 unit_id_to_name: dict[int, str]):
        self.__units_statistics = heated_shelf_orders_and_couriers_statistics.units
        self.__error_unit_ids = heated_shelf_orders_and_couriers_statistics.error_unit_ids
        self.__unit_id_to_name = unit_id_to_name

    def get_sorted_units_statistics(self) -> list[models.UnitHeatedShelfOrdersAndCouriers]:
        return sorted(self.__units_statistics, reverse=True,
                      key=lambda unit: (unit.awaiting_orders_count, unit.in_queue_count, unit.total_count))

    def get_text(self) -> str:
        lines = ['<b>Остывают на полке - В очереди (Всего):</b>']
        for unit in self.get_sorted_units_statistics():
            unit_name = self.__unit_id_to_name[unit.unit_id]
            lines.append(f'{unit_name}'
                         f' | {unit.awaiting_orders_count}'
                         f' - {unit.in_queue_count}'
                         f' ({unit.total_count})')
        return '\n'.join(lines)
