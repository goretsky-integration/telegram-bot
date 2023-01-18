import asyncio
from typing import Callable, Iterable, Any
from uuid import UUID

import httpx
from pydantic import parse_obj_as

import models.api_responses.auth as auth_models
import models.api_responses.dodo as models
from core import exceptions
from services.api_responses import decode_response_json_or_raise_error
from services.converters import UnitsConverter
from shortcuts import flatten

__all__ = (
    'DodoAPIService',
    'get_v1_statistics_reports_batch',
    'get_v2_statistics_reports_batch',
)


class DodoAPIService:
    __slots__ = ('_http_client_factory', '_country_code')

    def __init__(self, *, http_client_factory: Callable[[], httpx.AsyncClient], country_code: str):
        self._http_client_factory = http_client_factory
        self._country_code = country_code

    async def get_revenue_statistics_report(self, unit_ids: Iterable[int]) -> models.RevenueStatisticsReport:
        url = f'/v1/{self._country_code}/reports/revenue'
        request_query_params = {'unit_ids': tuple(unit_ids)}
        async with self._http_client_factory() as client:
            response = await client.get(url, params=request_query_params)
        return models.RevenueStatisticsReport.parse_obj(response.json())

    async def __get_v2_statistics_report(self, *, resource: str, unit_uuids: Iterable[UUID], access_token: str):
        url = f'/v2/{self._country_code}/reports/{resource}'
        request_query_params = {'unit_uuids': tuple(unit_uuids)}
        request_headers = {'Authorization': f'Bearer {access_token}'}
        async with self._http_client_factory() as client:
            response = await client.get(url, params=request_query_params, headers=request_headers)
        response_data = decode_response_json_or_raise_error(response)
        if response.status_code != 200:
            raise exceptions.DodoAPIServiceError
        return response_data

    async def get_late_delivery_vouchers_statistics_report(
            self,
            *,
            unit_uuids: Iterable[UUID],
            access_token: str,
    ) -> tuple[models.UnitLateDeliveryVouchersStatisticsReport, ...]:
        response_data = await self.__get_v2_statistics_report(
            resource='being-late-certificates',
            unit_uuids=unit_uuids,
            access_token=access_token,
        )
        return parse_obj_as(tuple[models.UnitLateDeliveryVouchersStatisticsReport, ...], response_data)

    async def get_delivery_productivity_statistics_report(
            self,
            *,
            unit_uuids: Iterable[UUID],
            access_token: str,
    ) -> tuple[models.UnitDeliveryProductivityStatisticsReport, ...]:
        response_data = await self.__get_v2_statistics_report(
            resource='delivery-productivity',
            unit_uuids=unit_uuids,
            access_token=access_token,
        )
        return parse_obj_as(tuple[models.UnitDeliveryProductivityStatisticsReport, ...], response_data)

    async def get_delivery_speed_statistics_report(
            self,
            *,
            unit_uuids: Iterable[UUID],
            access_token: str,
    ) -> tuple[models.UnitDeliverySpeedStatisticsReport]:
        response_data = await self.__get_v2_statistics_report(
            resource='delivery-speed',
            unit_uuids=unit_uuids,
            access_token=access_token,
        )
        return parse_obj_as(tuple[models.UnitDeliverySpeedStatisticsReport, ...], response_data)

    async def get_heated_shelf_time_statistics_report(
            self,
            *,
            unit_uuids: Iterable[UUID],
            access_token: str,
    ) -> tuple[models.UnitHeatedShelfTimeStatisticsReport, ...]:
        response_data = await self.__get_v2_statistics_report(
            resource='heated-shelf-time',
            unit_uuids=unit_uuids,
            access_token=access_token,
        )
        return parse_obj_as(tuple[models.UnitHeatedShelfTimeStatisticsReport, ...], response_data)

    async def get_restaurant_cooking_time_statistics_report(
            self,
            *,
            unit_uuids: Iterable[UUID],
            access_token: str,
    ) -> tuple[models.UnitRestaurantCookingTimeStatisticsReport, ...]:
        response_data = await self.__get_v2_statistics_report(
            resource='restaurant-cooking-time',
            unit_uuids=unit_uuids,
            access_token=access_token,
        )
        return parse_obj_as(tuple[models.UnitRestaurantCookingTimeStatisticsReport, ...], response_data)

    async def get_productivity_balance_statistics_report(
            self,
            *,
            unit_uuids: Iterable[UUID],
            access_token: str,
    ) -> tuple[models.UnitProductivityBalanceStatisticsReport, ...]:
        response_data = await self.__get_v2_statistics_report(
            resource='productivity-balance',
            unit_uuids=unit_uuids,
            access_token=access_token,
        )
        return parse_obj_as(tuple[models.UnitProductivityBalanceStatisticsReport, ...], response_data)

    async def __get_v1_statistics_report(self, *, resource: str, unit_ids: Iterable[int], cookies: dict):
        url = f'/v1/reports/{resource}'
        request_body = {
            'cookies': cookies,
            'unit_ids': tuple(unit_ids),
        }
        async with self._http_client_factory() as client:
            response = await client.post(url, json=request_body)
        response_data = decode_response_json_or_raise_error(response)
        if response.status_code != 200:
            raise exceptions.DodoAPIServiceError
        return response_data

    async def get_trips_with_one_order_statistics_report(
            self,
            *,
            unit_ids: Iterable[int],
            cookies: dict,
    ) -> tuple[models.UnitTripsWithOneOrderStatisticsReport, ...]:
        response_data = await self.__get_v1_statistics_report(
            resource='trips-with-one-order',
            unit_ids=unit_ids,
            cookies=cookies
        )
        return parse_obj_as(tuple[models.UnitTripsWithOneOrderStatisticsReport, ...], response_data)

    async def get_bonus_system_statistics_report(self, *, unit_ids: Iterable[int], cookies: dict):
        return await self.__get_v1_statistics_report(
            resource='bonus-system',
            unit_ids=unit_ids,
            cookies=cookies
        )

    async def get_kitchen_productivity_statistics_report(
            self,
            *,
            unit_ids: Iterable[int],
            cookies: dict,
    ) -> models.KitchenProductivityStatisticsReport:
        response_data = await self.__get_v1_statistics_report(
            resource='kitchen-productivity',
            unit_ids=unit_ids,
            cookies=cookies
        )
        return models.KitchenProductivityStatisticsReport.parse_obj(response_data)

    async def get_awaiting_orders_statistics_report(
            self,
            *,
            unit_ids: Iterable[int],
            cookies: dict,
    ) -> models.AwaitingOrdersStatisticsReport:
        response_data = await self.__get_v1_statistics_report(
            resource='awaiting-orders',
            unit_ids=unit_ids,
            cookies=cookies
        )
        return models.AwaitingOrdersStatisticsReport.parse_obj(response_data)


async def get_v1_statistics_reports_batch(
        *,
        api_method: Callable,
        units_grouped_by_account_name: dict[str, UnitsConverter],
        accounts_cookies: Iterable[auth_models.AccountCookies],
) -> tuple[Any, ...]:
    tasks = [
        api_method(
            unit_ids=units_grouped_by_account_name[account_cookies.account_name].ids,
            cookies=account_cookies.cookies,
        ) for account_cookies in accounts_cookies
    ]
    statistics_reports: tuple[Any, ...] = await asyncio.gather(*tasks)
    return statistics_reports


async def get_v2_statistics_reports_batch(
        *,
        api_method: Callable,
        units_grouped_by_account_name: dict[str, UnitsConverter],
        accounts_tokens: Iterable[auth_models.AccountTokens],
):
    tasks = [
        api_method(
            unit_uuids=units_grouped_by_account_name[account_tokens.account_name].uuids,
            access_token=account_tokens.access_token,
        ) for account_tokens in accounts_tokens
    ]
    reports: tuple[Any, ...] = await asyncio.gather(*tasks)
    return flatten(reports)
