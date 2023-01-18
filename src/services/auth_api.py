import asyncio
from typing import Callable, Iterable

import httpx

import models.api_responses.auth as auth_models
from core import exceptions
from services.api_responses import decode_response_json_or_raise_error

__all__ = ('AuthAPIService', 'get_cookies_batch')


class AuthAPIService:
    __slots__ = ('_http_client_factory',)

    def __init__(self, http_client_factory: Callable[[], httpx.AsyncClient]):
        self._http_client_factory = http_client_factory

    async def get_account_tokens(self, account_name: str) -> auth_models.AccountTokens:
        request_query_params = {'account_name': account_name}
        async with self._http_client_factory() as client:
            response = await client.get('/auth/token/', params=request_query_params)
        response_data = decode_response_json_or_raise_error(response)
        if response.status_code != 200:
            raise exceptions.AuthAPIServiceError(account_name=account_name)
        return auth_models.AccountTokens.parse_obj(response_data)

    async def get_account_cookies(self, account_name: str) -> auth_models.AccountCookies:
        request_query_params = {'account_name': account_name}
        async with self._http_client_factory() as client:
            response = await client.get('/auth/cookies/', params=request_query_params)
        response_data = decode_response_json_or_raise_error(response)
        if response.status_code != 200:
            raise exceptions.AuthAPIServiceError(account_name=account_name)
        return auth_models.AccountCookies.parse_obj(response_data)


async def get_cookies_batch(
        *,
        auth_api_service: AuthAPIService,
        account_names: Iterable[str],
) -> tuple[auth_models.AccountCookies, ...]:
    tasks = (auth_api_service.get_account_cookies(account_name) for account_name in account_names)
    accounts_cookies: tuple[auth_models.AccountCookies, ...] = await asyncio.gather(*tasks)
    return accounts_cookies
