from typing import Iterable

from pydantic import parse_obj_as

import models
from repositories.base import BaseHTTPAPIRepository
from utils import exceptions

__all__ = (
    'DatabaseRepository',
)


class DatabaseRepository(BaseHTTPAPIRepository):

    async def get_report_types(self) -> list[models.ReportType]:
        response = await self._client.get('/report-types/', timeout=30)
        if response.is_error:
            raise exceptions.DatabaseAPIError
        return parse_obj_as(list[models.ReportType], response.json())

    async def get_statistics_report_types(self) -> list[models.StatisticsReportType]:
        response = await self._client.get('/report-types/statistics/', timeout=30)
        if response.is_error:
            raise exceptions.DatabaseAPIError
        return parse_obj_as(list[models.StatisticsReportType], response.json())

    async def get_units(self, region: str | None = None) -> list[models.Unit]:
        params = {'region': region} if region is not None else {}
        response = await self._client.get('/units/', params=params, timeout=30)
        if response.is_error:
            raise exceptions.DatabaseAPIError
        return parse_obj_as(list[models.Unit], response.json())

    async def get_regions(self) -> list[str]:
        response = await self._client.get('/units/regions/', timeout=30)
        if response.is_error:
            raise exceptions.DatabaseAPIError
        return response.json()

    async def get_reports(self, report_type: str | None = None, chat_id: int | None = None) -> list[models.Report]:
        params = {'chat_id': chat_id, 'report_type': report_type}
        response = await self._client.get('/reports/', params=params, timeout=30)
        if response.is_error:
            raise exceptions.DatabaseAPIError
        return parse_obj_as(list[models.Report], response.json())

    async def add_unit_id_to_report(self, report_type: str, chat_id: int, unit_ids: Iterable[int]):
        body = {
            'report_type': report_type,
            'chat_id': chat_id,
            'unit_ids': tuple(unit_ids),
        }
        await self._client.post('/reports/', json=body, timeout=30)

    async def remove_unit_id_from_report(self, report_type: str, chat_id: int, unit_ids: Iterable[int]):
        body = {
            'report_type': report_type,
            'chat_id': chat_id,
            'unit_ids': tuple(unit_ids),
        }
        await self._client.request('DELETE', '/reports/', json=body, timeout=30)
