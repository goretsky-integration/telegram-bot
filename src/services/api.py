from typing import Iterable, Sequence

import httpx

import models
from config import app_settings
from utils import exceptions


async def get_revenue_statistics(
        unit_ids: Iterable[int] | Sequence[int],
) -> models.UnitsRevenueStatistics:
    url = f'{app_settings.api_url}/v1/statistics/revenue'
    params = {'unit_ids': list(unit_ids)}
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=15)
        except httpx.HTTPError:
            raise exceptions.DodoAPIError
    if not response.is_success:
        raise exceptions.DodoAPIError
    return models.UnitsRevenueStatistics.parse_obj(response.json())


async def get_kitchen_statistics(
        unit_ids: Iterable[int],
        cookies: dict,
) -> models.KitchenStatisticsBatch:
    url = f'{app_settings.api_url}/v1/statistics/kitchen'
    body = {'cookies': cookies, 'unit_ids': unit_ids}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=body, timeout=30)
        except httpx.HTTPError:
            raise exceptions.DodoAPIError

    if not response.is_success:
        raise exceptions.DodoAPIError

    return models.KitchenStatisticsBatch.parse_obj(response.json())