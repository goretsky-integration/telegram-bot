from abc import ABC, abstractmethod
from typing import Type

import db
import models
import responses
from responses.base import Response
from services import api
from utils import exceptions


class StatisticsReportStrategy(ABC):

    def __init__(self, report_type: str, chat_id: int, unit_id_to_name: dict[int, str]):
        self._report_type = report_type
        self._chat_id = chat_id
        self._unit_id_to_name = unit_id_to_name

    async def get_enabled_unit_ids(self) -> list[int]:
        unit_ids = await db.get_unit_ids_by_report_type_and_chat_id(models.ReportType.STATISTICS.name, self._chat_id)
        if not unit_ids:
            raise exceptions.NoneUnitIdsSetUpError
        return unit_ids

    @abstractmethod
    async def get_statistics_report(self) -> Response:
        pass


class DailyRevenueStatistics(StatisticsReportStrategy):

    async def get_statistics_report(self) -> responses.RevenueStatistics:
        unit_ids = await self.get_enabled_unit_ids()
        revenue_statistics = await api.get_revenue_statistics(unit_ids)
        return responses.RevenueStatistics(revenue_statistics, self._unit_id_to_name)


report_type_to_strategy: dict[str, Type[StatisticsReportStrategy]] = {
    models.StatisticsReportType.DAILY_REVENUE.name: DailyRevenueStatistics
}
