from responses.base import Response, ReplyMarkup
from keyboards import PeriodsMarkup

__all__ = (
    'WriteOffsReportPeriodResponse',
)


class WriteOffsReportPeriodResponse(Response):

    def get_text(self) -> str:
        return 'Выберите период, за который нужно загрузить отчет о списаниях'

    def get_reply_markup(self) -> ReplyMarkup:
        return PeriodsMarkup()
