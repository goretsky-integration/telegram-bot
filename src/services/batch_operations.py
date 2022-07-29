import asyncio
from typing import Iterable, TypeVar
from uuid import UUID

import models
from repositories import AuthCredentialsRepository
from utils import exceptions

__all__ = (
    'get_tokens_batch',
    'get_cookies_batch',
    'get_statistics_batch_by_unit_ids',
    'get_statistics_batch_by_unit_uuids',
    'get_statistics_batch_by_unit_ids_and_names',
)

_T = TypeVar('_T')


async def get_cookies_batch(
        auth_client: AuthCredentialsRepository,
        account_names: Iterable[str],
) -> tuple[models.AuthCookies | exceptions.NoCookiesError, ...]:
    tasks = (auth_client.get_cookies(account_name) for account_name in account_names)
    return await asyncio.gather(*tasks, return_exceptions=True)


async def get_tokens_batch(
        auth_client: AuthCredentialsRepository,
        account_names: Iterable[str],
) -> tuple[models.AuthToken | exceptions.NoTokenError, ...]:
    tasks = (auth_client.get_tokens(account_name) for account_name in account_names)
    return await asyncio.gather(*tasks, return_exceptions=True)


async def get_statistics_batch_by_unit_ids(
        dodo_client_method,
        dodo_client,
        accounts_cookies: Iterable[models.AuthCookies | exceptions.NoCookiesError],
        account_names_to_unit_ids,
        response_model: _T,
) -> _T:
    account_name_to_account_cookies: dict[str, models.AuthCookies | exceptions.NoCookiesError] = {
        account_cookies.account_name: account_cookies for account_cookies in accounts_cookies
        if not isinstance(account_cookies, exceptions.NoCookiesError)}

    tasks = []
    error_unit_ids: list[int] = []
    units_statistics: list = []

    for account_name, unit_ids in account_names_to_unit_ids.items():
        account_cookies = account_name_to_account_cookies[account_name]
        if isinstance(account_cookies, exceptions.NoCookiesError):
            error_unit_ids += unit_ids
        else:
            tasks.append(dodo_client_method(dodo_client, account_cookies.cookies, unit_ids))

    responses: tuple[_T, ...] = await asyncio.gather(*tasks, return_exceptions=True)

    for statistics_response in responses:
        if isinstance(statistics_response, exceptions.DodoAPIRequestByUnitIdsError):
            error_unit_ids += statistics_response.unit_ids
        else:
            units_statistics += statistics_response.units
            error_unit_ids += statistics_response.error_unit_ids
    return response_model(units=units_statistics, error_unit_ids=error_unit_ids)


async def get_statistics_batch_by_unit_uuids(
        dodo_client_method,
        dodo_client,
        account_tokens: Iterable[models.AuthToken | exceptions.NoCookiesError],
        account_names_to_unit_uuids,
        response_model: _T,
) -> _T:
    account_name_to_account_tokens: dict[str, models.AuthToken | exceptions.NoTokenError] = {
        account_tokens.account_name: account_tokens for account_tokens in account_tokens
        if not isinstance(account_tokens, exceptions.NoCookiesError)}

    tasks = []
    error_unit_uuids: list[UUID] = []
    units_statistics: list = []

    for account_name, unit_uuids in account_names_to_unit_uuids.items():
        account_token = account_name_to_account_tokens[account_name]
        if isinstance(account_token, exceptions.NoTokenError):
            error_unit_uuids += unit_uuids
        else:
            tasks.append(dodo_client_method(dodo_client, account_token.access_token, unit_uuids))

    responses: tuple[list[_T] | exceptions.DodoAPIRequestByUnitUUIDsError, ...] = await asyncio.gather(*tasks, return_exceptions=True)

    for statistics_response in responses:
        if isinstance(statistics_response, exceptions.DodoAPIRequestByUnitUUIDsError):
            error_unit_uuids += statistics_response.unit_uuids
        else:
            units_statistics += statistics_response
    return response_model(units=units_statistics, error_unit_uuids=error_unit_uuids)


async def get_statistics_batch_by_unit_ids_and_names(
        dodo_client_method,
        dodo_client,
        accounts_cookies: Iterable[models.AuthCookies | exceptions.NoCookiesError],
        account_names_to_unit_ids_and_names: dict[str, Iterable[models.UnitIdAndName]],
        response_model: _T,
):
    account_name_to_account_cookies: dict[str, models.AuthCookies | exceptions.NoCookiesError] = {
        account_cookies.account_name: account_cookies for account_cookies in accounts_cookies
        if not isinstance(account_cookies, exceptions.NoCookiesError)}

    tasks = []
    error_unit_ids_and_names: list[models.UnitIdAndName] = []
    units_statistics: list = []

    for account_name, unit_id_and_name in account_names_to_unit_ids_and_names.items():
        account_cookies = account_name_to_account_cookies[account_name]
        if isinstance(account_cookies, exceptions.NoCookiesError):
            error_unit_ids_and_names += unit_id_and_name
        else:
            tasks.append(dodo_client_method(dodo_client, account_cookies.cookies, unit_id_and_name))

    responses = await asyncio.gather(*tasks, return_exceptions=True)

    for statistics_response in responses:
        if isinstance(statistics_response, exceptions.DodoAPIRequestByUnitIdsAndNamesError):
            error_unit_ids_and_names += statistics_response.unit_ids_and_names
        else:
            units_statistics += statistics_response
    return response_model(units=units_statistics, error_unit_ids_and_names=error_unit_ids_and_names)
