import asyncio
import datetime
from typing import Callable, Iterable, Any
from uuid import UUID

import dodo_is_api.models as dodo_is_api_models
from dodo_is_api.connection import AsyncDodoISAPIConnection
from dodo_is_api.connection.http_clients import closing_async_httpx_client
from dodo_is_api.mappers import map_courier_order_dto
from pydantic import parse_obj_as

import models.api_responses.auth as auth_models
import models.api_responses.dodo as models
from core import exceptions
from services.api_responses import decode_response_json_or_raise_error
from services.converters import UnitsConverter
from services.http_client_factory import HTTPClient

__all__ = (
    'DodoAPIService',
    'get_v1_statistics_reports_batch',
    'get_v2_statistics_reports_batch',
    'get_bonus_system_statistics_reports_batch',
    'get_courier_orders',
)

from services.period import Period


class DodoAPIService:
    __slots__ = ('__http_client', '__country_code')

    def __init__(self, http_client: HTTPClient, country_code: str):
        self.__http_client = http_client
        self.__country_code = country_code

    async def get_revenue_statistics_report(self, unit_ids: Iterable[
        int]) -> models.RevenueStatisticsReport:
        url = f'/v1/{self.__country_code}/reports/revenue'
        request_query_params = {'unit_ids': tuple(unit_ids)}
        response = await self.__http_client.get(
            url=url,
            params=request_query_params,
        )
        return models.RevenueStatisticsReport.parse_obj(response.json())

    async def __get_v2_statistics_report(self, *, resource: str,
                                         unit_uuids: Iterable[UUID],
                                         access_token: str):
        url = f'/v2/{self.__country_code}/reports/{resource}'
        request_query_params = {'unit_uuids': tuple(unit_uuids)}
        request_headers = {'Authorization': f'Bearer {access_token}'}
        response = await self.__http_client.get(url,
                                                params=request_query_params,
                                                headers=request_headers)
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
        return parse_obj_as(
            tuple[models.UnitLateDeliveryVouchersStatisticsReport, ...],
            response_data)

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
        return parse_obj_as(
            tuple[models.UnitDeliveryProductivityStatisticsReport, ...],
            response_data)

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
        return parse_obj_as(
            tuple[models.UnitDeliverySpeedStatisticsReport, ...], response_data)

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
        return parse_obj_as(
            tuple[models.UnitHeatedShelfTimeStatisticsReport, ...],
            response_data)

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
        return parse_obj_as(
            tuple[models.UnitRestaurantCookingTimeStatisticsReport, ...],
            response_data)

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
        return parse_obj_as(
            tuple[models.UnitProductivityBalanceStatisticsReport, ...],
            response_data)

    async def __get_v1_statistics_report(self, *, resource: str,
                                         unit_ids: Iterable[int],
                                         cookies: dict):
        url = f'/v1/{self.__country_code}/reports/{resource}'
        request_query_params = {'unit_ids': tuple(unit_ids)}
        response = await self.__http_client.get(url, cookies=cookies,
                                                params=request_query_params)
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
        return parse_obj_as(
            tuple[models.UnitTripsWithOneOrderStatisticsReport, ...],
            response_data)

    async def get_bonus_system_statistics_report(
            self,
            *,
            unit_ids_and_names: Iterable[dict],
            cookies: dict,
    ) -> tuple[models.UnitBonusSystemStatisticsReport, ...]:
        url = f'/v1/{self.__country_code}/reports/bonus-system'
        request_body = tuple(unit_ids_and_names)
        response = await self.__http_client.post(url, cookies=cookies,
                                                 json=request_body)
        response_data = decode_response_json_or_raise_error(response)
        if response.status_code != 200:
            raise exceptions.DodoAPIServiceError
        return parse_obj_as(tuple[models.UnitBonusSystemStatisticsReport, ...],
                            response_data)

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
        return models.KitchenProductivityStatisticsReport.parse_obj(
            response_data)

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
) -> list[Any]:
    async with asyncio.TaskGroup() as task_group:
        tasks = [
            task_group.create_task(api_method(
                unit_ids=units_grouped_by_account_name[
                    account_cookies.account_name].ids,
                cookies=account_cookies.cookies,
            )) for account_cookies in accounts_cookies
        ]
    return [task.result() for task in tasks]


async def get_bonus_system_statistics_reports_batch(
        *,
        dodo_api_service: DodoAPIService,
        units_grouped_by_account_name: dict[str, UnitsConverter],
        accounts_cookies: Iterable[auth_models.AccountCookies],
) -> list[models.UnitBonusSystemStatisticsReport]:
    async with asyncio.TaskGroup() as task_group:
        tasks = [
            task_group.create_task(
                dodo_api_service.get_bonus_system_statistics_report(
                    unit_ids_and_names=units_grouped_by_account_name[
                        account_cookies.account_name].ids_and_names,
                    cookies=account_cookies.cookies,
                )) for account_cookies in accounts_cookies
        ]
    return [result for task in tasks for result in task.result()]


async def get_v2_statistics_reports_batch(
        *,
        api_method: Callable,
        units_grouped_by_account_name: dict[str, UnitsConverter],
        accounts_tokens: Iterable[auth_models.AccountTokens],
):
    async with asyncio.TaskGroup() as task_group:
        tasks = [
            task_group.create_task(api_method(
                unit_uuids=units_grouped_by_account_name[
                    account_tokens.account_name].uuids,
                access_token=account_tokens.access_token,
            )) for account_tokens in accounts_tokens
        ]
    return [result for task in tasks for result in task.result()]


async def request_courier_orders_from_dodo_is_api(
        period: Period,
        unit_uuids: Iterable[UUID],
        access_token: str,
        country_code: str,
) -> list[dodo_is_api_models.CourierOrder]:
    async with closing_async_httpx_client(
            access_token=access_token,
            country_code=country_code,
    ) as http_client:
        connection = AsyncDodoISAPIConnection(http_client=http_client)
        courier_orders_iterator = connection.iter_courier_orders(
            from_date=period.start + datetime.timedelta(hours=3),
            to_date=period.end + datetime.timedelta(hours=3),
            units=unit_uuids,
        )

        return [
            map_courier_order_dto(courier_order)
            async for courier_orders in courier_orders_iterator
            for courier_order in courier_orders
        ]


async def get_courier_orders(
        *,
        period: Period,
        units: UnitsConverter,
        country_code: str,
        dodo_is_api_credentials: Iterable[auth_models.AccountTokens],
) -> list[dodo_is_api_models.CourierOrder]:
    units_grouped_by_account_name = units.grouped_by_dodo_is_api_account_name
    account_name_to_access_token = {
        credentials.account_name: credentials.access_token
        for credentials in dodo_is_api_credentials
    }

    async with asyncio.TaskGroup() as task_group:
        tasks = [
            task_group.create_task(
                request_courier_orders_from_dodo_is_api(
                    period=period,
                    unit_uuids=units.uuids,
                    country_code=country_code,
                    access_token=account_name_to_access_token[account_name],
                )
            ) for account_name, units in units_grouped_by_account_name.items()
        ]

    return [
        courier_order
        for task in tasks
        for courier_order in task.result()
    ]
