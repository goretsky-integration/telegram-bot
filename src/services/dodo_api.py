from typing import Callable, Iterable

import httpx

import models.api_responses.dodo as models

__all__ = ('DodoAPIService',)


class DodoAPIService:

    def __init__(self, *, http_client_factory: Callable[[], httpx.AsyncClient], country_code: str):
        self._http_client_factory = http_client_factory
        self._country_code = country_code

    async def get_revenue_statistics_report(self, unit_ids: Iterable[int]) -> models.RevenueStatisticsReport:
        url = f'/v1/{self._country_code}/reports/revenue'
        request_query_params = {'unit_ids': tuple(unit_ids)}
        async with self._http_client_factory() as client:
            response = await client.get(url, params=request_query_params)
        return models.RevenueStatisticsReport.parse_obj(response.json())
