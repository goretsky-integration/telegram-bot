import keyboards
import models.database
from models import api
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
