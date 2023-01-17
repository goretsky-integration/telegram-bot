from typing import Callable

import httpx

import models.api_responses.auth as models
from core import exceptions
from services.api_responses import decode_response_json_or_raise_error

__all__ = ('AuthAPIService',)


class AuthAPIService:
    __slots__ = ('_http_client_factory',)

    def __init__(self, http_client_factory: Callable[[], httpx.AsyncClient]):
        self._http_client_factory = http_client_factory

    async def get_account_tokens(self, account_name: str) -> models.AccountTokens:
        request_query_params = {'account_name': account_name}
        async with self._http_client_factory() as client:
            response = await client.get('/auth/token/', params=request_query_params)
        response_data = decode_response_json_or_raise_error(response)
        if response.status_code != 200:
            raise exceptions.AuthAPIServiceError(f'Could not retrieve tokens of account {account_name}')
        return models.AccountTokens.parse_obj(response_data)

    async def get_account_cookies(self, account_name: str) -> models.AccountCookies:
        request_query_params = {'account_name': account_name}
        async with self._http_client_factory() as client:
            response = await client.get('/auth/cookies/', params=request_query_params)
        response_data = decode_response_json_or_raise_error(response)
        if response.status_code != 200:
            raise exceptions.AuthAPIServiceError(f'Could not retrieve cookies of account {account_name}')
        return models.AccountCookies.parse_obj(response_data)
