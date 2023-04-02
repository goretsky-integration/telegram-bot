from collections.abc import Iterable
from typing import AsyncGenerator, Never, Protocol

import httpx
from pydantic import parse_obj_as

import models.api_responses.database as models
from core import exceptions
from services.api_responses import decode_response_json_or_raise_error


class IChat(Protocol):
    id: int
    type: str
    username: str | None

    @property
    def full_name(self) -> str: ...


def handle_set_user_role_response(
        *,
        chat_id: int,
        response: httpx.Response,
) -> None | Never:
    if response.status_code == 204:
        return

    response_data = decode_response_json_or_raise_error(response)
    match (response.status_code, response_data):
        case [400, response_data]:
            raise exceptions.DatabaseAPIServiceError(
                'Invalid request to `set user role` api endpoint.'
                f' Response data: {response_data}'
            )
        case [404, {'message': 'Role is not found'}]:
            raise exceptions.RoleNotFoundError
        case [404, {'message': 'Chat by chat ID is not found'}]:
            raise exceptions.UserNotFoundError(chat_id=chat_id)


def handle_create_chat_response(response: httpx.Response) -> None | Never:
    if response.status_code == 201:
        return

    match response.status_code:
        case 400:
            raise exceptions.DatabaseAPIServiceError(
                'Invalid request to `create chat` api endpoint.'
            )
        case 409:
            raise exceptions.UserAlreadyExistsError


class DatabaseAPIService:
    __slots__ = ('__http_client',)

    def __init__(self, http_client: httpx.AsyncClient):
        self.__http_client = http_client

    async def set_user_role(
            self,
            *,
            chat_id: int,
            access_code: str,
    ) -> None | Never:
        url = f'/roles/users/{chat_id}/'
        request_body = {'access_code': access_code}
        response = await self.__http_client.patch(url, json=request_body)
        handle_set_user_role_response(chat_id=chat_id, response=response)

    async def iter_role_units(
            self,
            *,
            chat_id: int,
            region_id: int | None = None,
            limit: int | None = 100,
            offset: int | None = 0,
    ) -> AsyncGenerator[list[models.Unit], None]:
        url = f'/roles/users/{chat_id}/units/'
        request_query_params = {
            'limit': limit,
            'offset': offset,
        }
        if region_id is not None:
            request_query_params['region_id'] = region_id

        while True:
            response = await self.__http_client.get(
                url=url,
                params=request_query_params,
            )
            response_data = response.json()

            match (response.status_code, response_data):
                case [403, {'message': 'User has no any role'}]:
                    raise exceptions.UserHasNoRoleError

            request_query_params['offset'] += limit

            if units := response_data['units']:
                yield parse_obj_as(list[models.Unit], units)

            if response_data['is_end_of_list_reached']:
                break

    async def get_role_units(
            self,
            *,
            chat_id: int,
            region_id: int | None = None,
    ) -> list[models.Unit]:
        role_units_iterator = self.iter_role_units(
            chat_id=chat_id,
            region_id=region_id,
        )
        all_units: list[models.Unit] = []
        async for units in role_units_iterator:
            all_units += units
        return all_units

    async def iter_role_regions(
            self,
            *,
            chat_id: int,
            limit: int | None = 100,
            offset: int | None = 0,
    ) -> AsyncGenerator[list[models.Region], None]:
        if limit is None:
            limit = 100
        if offset is None:
            offset = 0

        url = f'/roles/users/{chat_id}/regions/'
        request_query_params = {
            'limit': limit,
            'offset': offset,
        }

        while True:
            response = await self.__http_client.get(
                url=url,
                params=request_query_params,
            )
            response_data = response.json()

            match (response.status_code, response_data):
                case [403, {'message': 'User has no any role'}]:
                    raise exceptions.UserHasNoRoleError

            request_query_params['offset'] += limit

            if regions := response_data['regions']:
                yield parse_obj_as(list[models.Region], regions)

            if response_data['is_end_of_list_reached']:
                break

    async def get_role_regions(self, *, chat_id: int) -> list[models.Region]:
        role_regions_iterator = self.iter_role_regions(chat_id=chat_id)
        all_regions: list[models.Region] = []
        async for regions in role_regions_iterator:
            all_regions += regions
        return all_regions

    async def iter_role_report_types(
            self,
            *,
            chat_id: int,
            limit: int | None = 100,
            offset: int | None = 0,
    ) -> AsyncGenerator[list[models.ReportType], None]:
        if limit is None:
            limit = 100
        if offset is None:
            offset = 0

        url = f'/roles/users/{chat_id}/report-types/'
        request_query_params = {
            'limit': limit,
            'offset': offset,
        }

        while True:
            response = await self.__http_client.get(
                url=url,
                params=request_query_params,
            )
            response_data = response.json()

            match (response.status_code, response_data):
                case [403, {'message': 'User has no any role'}]:
                    raise exceptions.UserHasNoRoleError

            request_query_params['offset'] += limit

            if report_types := response_data['report_types']:
                yield parse_obj_as(list[models.ReportType], report_types)

            if response_data['is_end_of_list_reached']:
                break

    async def get_role_report_types(
            self,
            *,
            chat_id: int,
    ) -> list[models.ReportType]:
        role_report_types = self.iter_role_report_types(chat_id=chat_id)
        all_report_types: list[models.ReportType] = []
        async for report_types in role_report_types:
            all_report_types += report_types
        return all_report_types

    async def iter_statistics_report_types(
            self,
            *,
            limit: int | None = 100,
            offset: int | None = 0,
    ) -> AsyncGenerator[list[models.ReportType], None]:
        if limit is None:
            limit = 100
        if offset is None:
            offset = 0

        url = f'/report-types/statistics/'
        request_query_params = {
            'limit': limit,
            'offset': offset,
        }

        while True:
            response = await self.__http_client.get(
                url=url,
                params=request_query_params,
            )
            response_data = response.json()

            request_query_params['offset'] += limit

            if report_types := response_data['report_types']:
                yield parse_obj_as(list[models.ReportType], report_types)

            if response_data['is_end_of_list_reached']:
                break

    async def get_statistics_report_types(self) -> list[models.ReportType]:
        report_types_iterator = self.iter_statistics_report_types()
        all_report_types: list[models.ReportType] = []
        async for report_types in report_types_iterator:
            all_report_types += report_types
        return all_report_types

    async def create_chat(self, chat: IChat) -> None | Never:
        url = '/telegram-chats/'
        request_data = {
            'chat_id': chat.id,
            'type': chat.type.upper(),
            'title': chat.full_name,
            'username': chat.username,
        }
        response = await self.__http_client.post(url, json=request_data)
        handle_create_chat_response(response)

    async def create_report_routes(
            self,
            *,
            report_type_id: int,
            chat_id: int,
            unit_ids: Iterable[int],
    ):
        url = '/report-routes/'
        request_data = {
            'report_type_id': report_type_id,
            'chat_id': chat_id,
            'unit_ids': tuple(unit_ids),
        }
        response = await self.__http_client.post(url, json=request_data)

    async def get_report_route_units(
            self,
            *,
            chat_id: int,
            report_type_id: int,
    ) -> list[int]:
        unit_ids_iterator = self.iter_report_route_units(
            chat_id=chat_id,
            report_type_id=report_type_id,
        )
        all_unit_ids = []
        async for unit_ids in unit_ids_iterator:
            all_unit_ids += unit_ids
        return all_unit_ids

    async def iter_report_route_units(
            self,
            *,
            chat_id: int,
            report_type_id: int,
            limit: int | None = 100,
            offset: int | None = 0
    ) -> AsyncGenerator[list[int], None]:
        url = f'/report-routes/units/'
        request_query_params = {
            'limit': limit,
            'offset': offset,
            'chat_id': chat_id,
            'report_type_id': report_type_id,
        }

        while True:
            response = await self.__http_client.get(
                url=url,
                params=request_query_params,
            )
            response_data = response.json()

            request_query_params['offset'] += limit

            if unit_ids := response_data['unit_ids']:
                yield unit_ids

            if response_data['is_end_of_list_reached']:
                break

    async def delete_report_routes(
            self,
            *,
            report_type_id: int,
            chat_id: int,
            unit_ids: Iterable[int],
    ):
        url = '/report-routes/'
        request_query_params = {
            'report_type_id': report_type_id,
            'chat_id': chat_id,
            'unit_ids': tuple(unit_ids),
        }
        response = await self.__http_client.delete(
            url=url,
            params=request_query_params,
        )

    async def get_report_type_by_name(self, name: str) -> models.ReportType:
        url = f'/report-types/names/{name}/'
        response = await self.__http_client.get(url)
        response_data = response.json()
        return models.ReportType.parse_obj(response_data)
