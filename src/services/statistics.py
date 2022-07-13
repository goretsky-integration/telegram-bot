import asyncio
import uuid
from typing import Iterable, Callable, Awaitable, TypeVar

import db
import models
from services import api

__all__ = (
    'get_delivery_speed_statistics',
    'get_being_late_certificates_statistics',
    'get_couriers_statistics',
    'get_heated_shelf_statistics',
    'get_kitchen_performance_statistics',
    'get_kitchen_production_statistics',
    'get_delivery_performance_statistics',
    'get_bonus_system_statistics',
    'get_revenue_statistics',
)

UM = TypeVar('UM')
RM = TypeVar('RM')


class StatisticsByCookiesAndUnitIds:

    def __init__(self, method: Callable[..., Awaitable],
                 unit_model: UM,
                 response_model: RM):
        self._unit_model = unit_model
        self._response_model = response_model
        self._method = method

    def _union_to_one_response_model(self, responses: Iterable[RM]) -> RM:
        units_statistics: list[models.UnitDeliveryPerformance] = []
        error_unit_ids: list[int] = []
        for response in responses:
            units_statistics += response.units
            error_unit_ids += response.error_unit_ids
        return self._response_model(units=units_statistics, error_unit_ids=error_unit_ids)

    async def _request(self, account_name: str, unit_ids: Iterable[int]) -> RM:
        cookies = await db.get_cookies(account_name)
        return await self._method(cookies, unit_ids)

    async def _request_all(self, account_names_to_unit_ids: dict[str, Iterable[int]]) -> tuple[RM, ...]:
        tasks = (self._request(account_name, unit_ids) for account_name, unit_ids in account_names_to_unit_ids.items())
        return await asyncio.gather(*tasks)

    async def _request_and_get_united_response_model(self, account_names_to_unit_ids: dict[str, Iterable[int]]) -> RM:
        responses = await self._request_all(account_names_to_unit_ids)
        return self._union_to_one_response_model(responses)

    def __call__(self, account_names_to_unit_ids: dict[str, Iterable[int]]):
        return self._request_and_get_united_response_model(account_names_to_unit_ids)


class StatisticsByCookiesAndUnitIdsAndNames:

    def __init__(self, method: Callable[..., Awaitable], unit_model: UM):
        self._method = method
        self._unit_model = unit_model

    @staticmethod
    def _flatten_unit_models(nested_responses: Iterable[Iterable[UM]]) -> list[UM]:
        return [response for responses in nested_responses for response in responses]

    async def _request(self, account_name: str, unit_ids_and_names: Iterable[models.UnitIdAndName]) -> RM:
        cookies = await db.get_cookies(account_name)
        return await self._method(cookies, unit_ids_and_names)

    async def _request_all(
            self, account_names_to_unit_ids_and_names: dict[str, Iterable[models.UnitIdAndName]],
    ) -> tuple[RM, ...]:
        tasks = (self._request(account_name, unit_ids_and_names)
                 for account_name, unit_ids_and_names in account_names_to_unit_ids_and_names.items())
        return await asyncio.gather(*tasks)

    async def _request_and_flatten_response_unit_models(
            self, account_names_to_unit_ids_and_names: dict[str, Iterable[models.UnitIdAndName]]
    ) -> list[RM]:
        nested_responses = await self._request_all(account_names_to_unit_ids_and_names)
        return self._flatten_unit_models(nested_responses)

    def __call__(self, account_names_to_unit_ids_and_names: dict[str, Iterable[models.UnitIdAndName]]):
        return self._request_and_flatten_response_unit_models(account_names_to_unit_ids_and_names)


async def get_delivery_speed_statistics(
        account_name_to_unit_uuids: dict[str, Iterable[uuid.UUID]],
) -> list[models.UnitDeliverySpeed]:
    tasks = []
    for account_name, unit_uuids in account_name_to_unit_uuids.items():
        token = await db.get_access_token(account_name)
        tasks.append(api.get_delivery_speed_statistics(token, unit_uuids))
    nested_responses: tuple[list[models.UnitDeliverySpeed], ...] = await asyncio.gather(*tasks)
    return [response for responses in nested_responses for response in responses]


get_being_late_certificates_statistics = StatisticsByCookiesAndUnitIdsAndNames(
    method=api.get_being_late_certificates_statistics,
    unit_model=models.UnitBeingLateCertificatesTodayAndWeekBefore,
)

get_bonus_system_statistics = StatisticsByCookiesAndUnitIdsAndNames(
    method=api.get_bonus_system_statistics,
    unit_model=models.UnitBonusSystem,
)

get_kitchen_production_statistics = StatisticsByCookiesAndUnitIds(
    method=api.get_kitchen_production_statistics,
    unit_model=models.UnitKitchenProduction,
    response_model=models.KitchenProductionStatistics,
)

get_delivery_performance_statistics = StatisticsByCookiesAndUnitIds(
    method=api.get_delivery_performance_statistics,
    unit_model=models.UnitDeliveryPerformance,
    response_model=models.DeliveryPerformanceStatistics,
)

get_kitchen_performance_statistics = StatisticsByCookiesAndUnitIds(
    method=api.get_kitchen_performance_statistics,
    unit_model=models.UnitKitchenPerformance,
    response_model=models.KitchenPerformanceStatistics,
)

get_heated_shelf_statistics = StatisticsByCookiesAndUnitIds(
    method=api.get_heated_shelf_statistics,
    unit_model=models.UnitHeatedShelf,
    response_model=models.HeatedShelfStatistics,
)

get_couriers_statistics = StatisticsByCookiesAndUnitIds(
    method=api.get_couriers_statistics,
    unit_model=models.UnitCouriers,
    response_model=models.CouriersStatistics,
)

get_revenue_statistics = api.get_revenue_statistics
