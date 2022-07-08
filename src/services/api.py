import asyncio
import uuid
from typing import Iterable, Sequence

import httpx
from pydantic import parse_obj_as

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


async def get_delivery_statistics(
        access_token: str,
        unit_uuids: Iterable[str | uuid.UUID],
) -> list[models.UnitDeliveryStatistics]:
    url = f'{app_settings.api_url}/v1/statistics/delivery'
    params = {'token': access_token, 'unit_uuids': tuple(unit_uuids)}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, params=params, timeout=30)
        except httpx.HTTPError:
            raise exceptions.DodoAPIError

    if not response.is_success:
        raise exceptions.DodoAPIError

    return parse_obj_as(list[models.UnitDeliveryStatistics], response.json())


async def get_being_late_certificates_statistics(
        unit_ids: Iterable[int] | Sequence[int], cookies: dict
) -> models.SingleUnitBeingLateCertificatesTodayAndWeekBefore\
     | list[models.UnitBeingLateCertificatesTodayAndWeekBefore]:
    """Get count of given certificates for delivery being late.

    Args:
        unit_ids: collection of unit ids.
        cookies: cookies as dict.

    Returns:
        `models.SingleUnitBeingLateCertificatesTodayAndWeekBefore` if only one unit id is specified in parameters,
        otherwise returns list of `models.UnitBeingLateCertificatesTodayAndWeekBefore`.
    """
    url = f'{app_settings.api_url}/v1/statistics/being-late-certificates/today-and-week-before'
    body = {'cookies': cookies, 'unit_ids': tuple(unit_ids)}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(url, json=body, timeout=30)
        except httpx.HTTPError:
            raise exceptions.DodoAPIError

    if not response.is_success:
        raise exceptions.DodoAPIError

    response_json = response.json()
    if isinstance(response_json, dict):
        response_json['unit_id'] = tuple(unit_ids)[0]
        return models.SingleUnitBeingLateCertificatesTodayAndWeekBefore.parse_obj(response_json)
    return parse_obj_as(list[models.UnitBeingLateCertificatesTodayAndWeekBefore], response_json)
