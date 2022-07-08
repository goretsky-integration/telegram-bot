from typing import Iterable

import keyboards
import models.database
from responses.base import Response, ReplyMarkup
from services.text_utils import humanize_percents, intgaps, humanize_seconds, abbreviate_unit_name


class RevenueStatistics(Response):

    def __init__(self, revenue_statistics: models.UnitsRevenueStatistics,
                 unit_id_to_name: dict[int, str]):
        self.__revenue_statistics = revenue_statistics
        self.__unit_id_to_name = unit_id_to_name

    def get_text(self) -> str | None:
        revenues = sorted(self.__revenue_statistics.revenues, reverse=True,
                          key=lambda report: report.today)
        lines = ['<b>Выручка за сегодня:</b>']

        for revenue in revenues:
            unit_name = self.__unit_id_to_name[revenue.unit_id]
            revenue_today = intgaps(revenue.today)
            delta_from_week_before = humanize_percents(round(revenue.delta_from_week_before))
            lines.append(f'{unit_name} | {revenue_today} | {delta_from_week_before}')

        total_revenue_today = intgaps(self.__revenue_statistics.metadata.total_revenue_today)
        delta_from_week_before = humanize_percents(round(self.__revenue_statistics.metadata.delta_from_week_before))
        lines.append(f'<b>Итого: {total_revenue_today} | {delta_from_week_before}</b>')

        return '\n'.join(lines)

    def get_reply_markup(self) -> ReplyMarkup | None:
        return keyboards.UpdateStatisticsReportMarkup(models.database.StatisticsReportType.DAILY_REVENUE.name)


class KitchenStatistics(Response):

    def __init__(self, kitchen_statistics: models.KitchenStatisticsBatch, unit_id_to_name: dict[int, str]):
        self.__kitchen_statistics = kitchen_statistics
        self.__unit_id_to_name = unit_id_to_name

    def get_text(self) -> str:
        kitchen_statistics = sorted(self.__kitchen_statistics.kitchen_statistics,
                                    key=lambda report: report.revenue.per_hour, reverse=True)
        lines = ['<b>Выручка на чел. в час</b>']

        for unit_kitchen_statistics in kitchen_statistics:
            unit_name = self.__unit_id_to_name[unit_kitchen_statistics.unit_id]
            revenue_per_hour = intgaps(unit_kitchen_statistics.revenue.per_hour)
            delta_from_week_before = humanize_percents(round(unit_kitchen_statistics.revenue.delta_from_week_before))
            lines.append(f'{unit_name} | {revenue_per_hour} | {delta_from_week_before}')

        for error_unit_id in self.__kitchen_statistics.error_unit_ids:
            unit_name = self.__unit_id_to_name[error_unit_id]
            lines.append(f'{unit_name} | <b>Ошибка</b>')

        return '\n'.join(lines)

    def get_reply_markup(self) -> ReplyMarkup:
        return keyboards.UpdateStatisticsReportMarkup(models.StatisticsReportType.KITCHEN_PERFORMANCE.name)


class DeliverySpeedStatistics(Response):

    def __init__(self, units_delivery_statistics: Iterable[models.UnitDeliveryStatistics]):
        self._units_delivery_statistics = units_delivery_statistics

    def get_text(self) -> str:
        units_delivery_statistics = sorted(self._units_delivery_statistics,
                                           key=lambda unit: unit.average_delivery_order_fulfillment_time)

        lines = ['<b>Общая скорость доставки - Время приготовления - Время на полке - Поездка курьера</b>']

        for unit_delivery_statistics in units_delivery_statistics:
            order_fulfillment_time = humanize_seconds(unit_delivery_statistics.average_delivery_order_fulfillment_time)
            cooking_time = humanize_seconds(unit_delivery_statistics.average_cooking_time)
            heated_shelf_time = humanize_seconds(unit_delivery_statistics.average_heated_shelf_time)
            order_trip_time = humanize_seconds(unit_delivery_statistics.average_order_trip_time)
            unit_name = abbreviate_unit_name(unit_delivery_statistics.unit_name)

            lines.append(f'{unit_name} | {order_fulfillment_time}'
                         f' | {cooking_time} | {heated_shelf_time} | {order_trip_time}')
        return '\n'.join(lines)

    def get_reply_markup(self) -> ReplyMarkup:
        return keyboards.UpdateStatisticsReportMarkup(models.StatisticsReportType.DELIVERY_SPEED.name)


class BeingLateCertificatesStatistics(Response):

    def __init__(self, being_late_certificates: Iterable[models.UnitBeingLateCertificatesTodayAndWeekBefore |
                                                         models.SingleUnitBeingLateCertificatesTodayAndWeekBefore],
                 unit_id_to_name: dict[int, str]):
        self._being_late_certificates = being_late_certificates
        self._unit_id_to_name = unit_id_to_name

    def get_text(self) -> str:
        lines = ['<b>Сертификаты за опоздание (сегодня) | (неделю назад)</b>']

        being_late_certificates = sorted(self._being_late_certificates, reverse=True,
                                         key=lambda i: (i.certificates_today_count, i.certificates_week_before_count))

        for report in being_late_certificates:
            if isinstance(report, models.SingleUnitBeingLateCertificatesTodayAndWeekBefore):
                unit_name = self._unit_id_to_name[report.unit_id]
            else:
                unit_name = report.unit_name
            lines.append(f'{unit_name} | {report.certificates_today_count} шт'
                         f' | {report.certificates_week_before_count} шт')

        return '\n'.join(lines)

    def get_reply_markup(self) -> ReplyMarkup:
        return keyboards.UpdateStatisticsReportMarkup(models.StatisticsReportType.BEING_LATE_CERTIFICATES.name)
