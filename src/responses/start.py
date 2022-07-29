from typing import Iterable

import keyboards
import models
from responses.base import Response, ReplyMarkup

__all__ = (
    'MainMenu',
    'StatisticsReportsMenu',
    'SettingsMenu',
)


class MainMenu(Response):

    def get_text(self) -> str | None:
        return 'Приветствую 👋'

    def get_reply_markup(self) -> ReplyMarkup | None:
        return keyboards.MainMenuMarkup()


class StatisticsReportsMenu(Response):

    def __init__(self, statistics_report_types: Iterable[models.StatisticsReportType]):
        self.statistics_report_types = statistics_report_types

    def get_text(self) -> str | None:
        return 'Выберите отчёт который хотите посмотреть 👇'

    def get_reply_markup(self) -> ReplyMarkup | None:
        return keyboards.StatisticsReportsMarkup(self.statistics_report_types)


class SettingsMenu(Response):

    def __init__(self, report_types: Iterable[models.ReportType]):
        self.report_types = report_types

    def get_text(self) -> str | None:
        return 'Выберите вид отчётов, которые хотите получать 👇'

    def get_reply_markup(self) -> ReplyMarkup | None:
        return keyboards.SettingsMarkup(self.report_types)
