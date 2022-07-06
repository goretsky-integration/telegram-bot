import keyboards
import models.database
from responses.base import Response, ReplyMarkup
from services.text_utils import humanize_percents, intgaps


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
