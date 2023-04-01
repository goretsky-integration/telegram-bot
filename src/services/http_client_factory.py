import contextlib
from typing import TypeAlias, Callable

import httpx

__all__ = ('HTTPClient', 'closing_http_client_factory', 'HTTPClientFactory')

HTTPClient: TypeAlias = httpx.AsyncClient
HTTPClientFactory: TypeAlias = Callable[..., HTTPClient]


@contextlib.asynccontextmanager
async def closing_http_client_factory(*, base_url: str) -> HTTPClient:
    async with httpx.AsyncClient(base_url=base_url, timeout=60) as client:
        yield client
