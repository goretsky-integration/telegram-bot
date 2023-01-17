import json

import httpx

from core import exceptions

__all__ = ('decode_response_json_or_raise_error',)


def decode_response_json_or_raise_error(response: httpx.Response) -> dict | list:
    try:
        return response.json()
    except json.JSONDecodeError:
        raise exceptions.JSONDecodeError
