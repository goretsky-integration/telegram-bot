from typing import Iterable

from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, InlineKeyboardMarkup
from dodolib import models

from keyboards import MainMenuMarkup, StatisticsReportsMarkup, SettingsMarkup
from views.base import BaseView

__all__ = (
    'ShowKeyboardView',
    'HideKeyboardView',
    'SettingsMenuView',
    'StatisticsReportsMenuView',
)


class ShowKeyboardView(BaseView):

    def get_text(self) -> str:
        return 'Приветствую 👋'

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        return MainMenuMarkup()


class HideKeyboardView(BaseView):

    def get_text(self) -> str:
        return 'Клавиатура спрятана 🙈'

    def get_reply_markup(self) -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove()


class StatisticsReportsMenuView(BaseView):

    def __init__(self, statistics_report_types: Iterable[models.StatisticsReportType]):
        self.statistics_report_types = statistics_report_types

    def get_text(self) -> str | None:
        return 'Выберите отчёт который хотите посмотреть 👇'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return StatisticsReportsMarkup(self.statistics_report_types)


class SettingsMenuView(BaseView):

    def __init__(self, report_types: Iterable[models.ReportType]):
        self.report_types = report_types

    def get_text(self) -> str | None:
        return 'Выберите вид отчётов, которые хотите получать 👇'

    def get_reply_markup(self) -> InlineKeyboardMarkup:
        return SettingsMarkup(self.report_types)
