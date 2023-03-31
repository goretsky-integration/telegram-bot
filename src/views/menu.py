from typing import Iterable

from aiogram.types import (
    ReplyKeyboardRemove, ReplyKeyboardMarkup,
    InlineKeyboardMarkup, KeyboardButton
)

import models.api_responses.database as models
from keyboards import StatisticsReportsMarkup, SettingsMarkup
from views.base import BaseView

__all__ = (
    'ShowKeyboardView',
    'HideKeyboardView',
    'SettingsMenuView',
    'StatisticsReportsMenuView',
)


class ShowKeyboardView(BaseView):
    text = 'Приветствую 👋'
    reply_markup = ReplyKeyboardMarkup(
        resize_keyboard=True,
        keyboard=[
            [
                KeyboardButton('📊 Отчёты/Статистика'),
            ],
            [
                KeyboardButton('⚙️ Настройки'),
                KeyboardButton('🙎‍♂️ Моя роль'),
            ],
        ]
    )


class HideKeyboardView(BaseView):

    def get_text(self) -> str:
        return 'Клавиатура спрятана 🙈'

    def get_reply_markup(self) -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove()


class StatisticsReportsMenuView(BaseView):

    def __init__(self, statistics_report_types: Iterable[models.ReportType]):
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
