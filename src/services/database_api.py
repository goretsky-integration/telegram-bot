from typing import Callable, Iterable

import httpx
from pydantic import parse_obj_as

import models.api_responses.database as models
from services.api_responses import decode_response_json_or_raise_error
from core import exceptions


class DatabaseAPIService:
    __slots__ = ('_http_client_factory',)

    def __init__(self, http_client_factory: Callable[[], httpx.AsyncClient]):
        self._http_client_factory = http_client_factory

    async def get_units(self, *, region: str | None = None) -> tuple[models.Unit, ...]:
        request_query_params = {}
        if region is not None:
            request_query_params['region'] = region
        async with self._http_client_factory() as client:
            response = await client.get('/units/', params=request_query_params)
        response_data = decode_response_json_or_raise_error(response)
        if response.status_code != 200:
            raise exceptions.DatabaseAPIServiceError('Could not retrieve units from database api.')
        return parse_obj_as(tuple[models.Unit, ...], response_data)

    async def get_regions(self) -> list[str]:
        async with self._http_client_factory() as client:
            response = await client.get('/units/regions/')
        response_data = decode_response_json_or_raise_error(response)
        if response.status_code != 200:
            raise exceptions.DatabaseAPIServiceError('Could not retrieve regions from database api.')
        return response_data

    async def get_reports_routes(
            self,
            *,
            report_type: str,
            chat_id: int | None = None,
    ) -> tuple[models.ReportRoute, ...]:
        request_query_params = {}
        if report_type is not None:
            request_query_params['report_type'] = report_type
        if chat_id is not None:
            request_query_params['chat_id'] = chat_id
        async with self._http_client_factory() as client:
            response = await client.get('/reports/', params=request_query_params)
        response_data = decode_response_json_or_raise_error(response)
        if response.status_code != 200:
            raise exceptions.DatabaseAPIServiceError('Could not retrieve report routes from database api.')
        return parse_obj_as(tuple[models.ReportRoute, ...], response_data)

    async def add_report_route(
            self,
            *,
            report_type: str,
            chat_id: int,
            unit_ids: Iterable[int],
    ) -> None:
        request_body = {'report_type': report_type, 'chat_id': chat_id, 'unit_ids': unit_ids}
        async with self._http_client_factory() as client:
            response = await client.post('/reports/', json=request_body)
        if response.is_error:
            raise exceptions.DatabaseAPIServiceError('Could not create report route in database api.')

    async def remove_report_route(
            self,
            *,
            report_type: str,
            chat_id: int,
            unit_ids: Iterable[int],
    ) -> None:
        request_params = {'report_type': report_type, 'chat_id': chat_id, 'unit_ids': unit_ids}
        async with self._http_client_factory() as client:
            response = await client.delete('/reports/', params=request_params)
        if response.is_error:
            raise exceptions.DatabaseAPIServiceError('Could not remove report route in database api.')

    async def __get_report_types(
            self,
            url: str,
    ) -> tuple[models.ReportType, ...]:
        async with self._http_client_factory() as client:
            response = await client.get(url)
        response_data = decode_response_json_or_raise_error(response)
        if response.status_code != 200:
            raise exceptions.DatabaseAPIServiceError('Could not retrieve report types')
        return parse_obj_as(tuple[models.ReportType, ...], response_data)

    async def get_report_types(self) -> tuple[models.ReportType, ...]:
        url = '/report-types/'
        return await self.__get_report_types(url)

    async def get_statistics_report_types(self) -> tuple[models.ReportType, ...]:
        url = '/report-types/statistics/'
        return await self.__get_report_types(url)
