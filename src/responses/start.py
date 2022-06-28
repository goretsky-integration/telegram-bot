import keyboards
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

    def get_text(self) -> str | None:
        return 'Выберите отчёт который хотите посмотреть 👇'

    def get_reply_markup(self) -> ReplyMarkup | None:
        return keyboards.StatisticsReportsMarkup()


class SettingsMenu(Response):

    def get_text(self) -> str | None:
        return 'Выберите вид отчётов, которые хотите получать 👇'

    def get_reply_markup(self) -> ReplyMarkup | None:
        return keyboards.SettingsMarkup()