from typing import Iterable, Sequence
from uuid import UUID

from pydantic import parse_obj_as

import models
from repositories.base import BaseHTTPAPIRepository
from utils import exceptions

__all__ = (
    'DodoAPIRepository',
)


class DodoAPIRepository(BaseHTTPAPIRepository):

    async def get_kitchen_performance_statistics(
            self,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
    ) -> models.KitchenPerformanceStatistics:
        body = {'cookies': cookies, 'unit_ids': tuple(unit_ids)}
        response = await self._client.post('/v1/statistics/kitchen/performance', json=body)
        if response.is_error:
            raise exceptions.DodoAPIRequestByUnitIdsError(unit_ids=unit_ids)
        return models.KitchenPerformanceStatistics.parse_obj(response.json())

    async def get_kitchen_production_statistics(
            self,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
    ) -> models.KitchenProductionStatistics:
        body = {'cookies': cookies, 'unit_ids': tuple(unit_ids)}
        response = await self._client.post('/v1/statistics/production/kitchen', json=body)
        if response.is_error:
            raise exceptions.DodoAPIRequestByUnitIdsError(unit_ids=unit_ids)
        return models.KitchenProductionStatistics.parse_obj(response.json())

    async def get_delivery_performance_statistics(
            self,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
    ) -> models.DeliveryPerformanceStatistics:
        body = {'cookies': cookies, 'unit_ids': tuple(unit_ids)}
        response = await self._client.post('/v1/statistics/delivery/performance', json=body)
        if response.is_error:
            raise exceptions.DodoAPIRequestByUnitIdsError(unit_ids=unit_ids)
        return models.DeliveryPerformanceStatistics.parse_obj(response.json())

    async def get_heated_shelf_statistics(
            self,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
    ) -> models.HeatedShelfStatistics:
        body = {'cookies': cookies, 'unit_ids': tuple(unit_ids)}
        response = await self._client.post('/v1/statistics/delivery/heated-shelf', json=body)
        if response.is_error:
            raise exceptions.DodoAPIRequestByUnitIdsError(unit_ids=unit_ids)
        return models.HeatedShelfStatistics.parse_obj(response.json())

    async def get_couriers_statistics(
            self,
            cookies: models.Cookies,
            unit_ids: Iterable[int],
    ) -> models.CouriersStatistics:
        body = {'cookies': cookies, 'unit_ids': tuple(unit_ids)}
        response = await self._client.post('/v1/statistics/delivery/couriers', json=body)
        if response.is_error:
            raise exceptions.DodoAPIRequestByUnitIdsError(unit_ids=unit_ids)
        return models.CouriersStatistics.parse_obj(response.json())

    async def get_revenue_statistics(
            self,
            unit_ids: Iterable[int] | Sequence[int],
    ) -> models.RevenueStatistics:
        url = '/v1/statistics/revenue'
        params = {'unit_ids': tuple(unit_ids)}
        response = await self._client.get(url, params=params, timeout=60)
        if response.is_error:
            raise exceptions.DodoAPIRequestByUnitIdsError(unit_ids=unit_ids)
        return models.RevenueStatistics.parse_obj(response.json())

    async def get_being_late_certificates_statistics(
            self,
            cookies: dict,
            unit_ids_and_names: Iterable[models.UnitIdAndName],
    ) -> list[models.UnitBeingLateCertificatesTodayAndWeekBefore]:
        url = '/v1/statistics/being-late-certificates'
        body = {'cookies': cookies, 'units': tuple(unit_ids_and_names)}
        response = await self._client.post(url, json=body)
        if response.is_error:
            raise exceptions.DodoAPIRequestByUnitIdsAndNamesError(unit_ids_and_names=unit_ids_and_names)
        return parse_obj_as(list[models.UnitBeingLateCertificatesTodayAndWeekBefore], response.json())

    async def get_bonus_system_statistics(
            self,
            cookies: dict,
            unit_ids_and_names: Iterable[models.UnitIdAndName],
    ) -> list[models.UnitBonusSystem]:
        url = '/v1/statistics/bonus-system'
        body = {'cookies': cookies, 'units': tuple(unit_ids_and_names)}
        response = await self._client.post(url, json=body)
        if response.is_error:
            raise exceptions.DodoAPIRequestByUnitIdsAndNamesError(unit_ids_and_names=unit_ids_and_names)
        return parse_obj_as(list[models.UnitBonusSystem], response.json())

    async def get_delivery_speed_statistics(
            self,
            token: str,
            unit_uuids: Iterable[UUID],
    ) -> list[models.UnitDeliverySpeed]:
        url = '/v2/statistics/delivery/speed'
        params = {'token': token, 'unit_uuids': [unit_uuid.hex for unit_uuid in unit_uuids]}
        response = await self._client.get(url, params=params)
        if response.is_error:
            raise exceptions.DodoAPIRequestByUnitUUIDsError(unit_uuids=unit_uuids)
        return parse_obj_as(list[models.UnitDeliverySpeed], response.json())

    async def get_orders_handover_time_statistics(
            self,
            token: str,
            unit_uuids: Iterable[UUID],
    ) -> list[models.UnitOrdersHandoverTime]:
        url = '/v2/statistics/production/handover-time'
        params = {'token': token, 'unit_uuids': [unit_uuid.hex for unit_uuid in unit_uuids],
                  'sales_channels': [models.SalesChannel.DINE_IN.value]}
        response = await self._client.get(url, params=params)
        if response.is_error:
            raise exceptions.DodoAPIRequestByUnitUUIDsError(unit_uuids=unit_uuids)
        return parse_obj_as(list[models.UnitOrdersHandoverTime], response.json())
