import httpx
import pytest

from services.http_client_factory import closing_http_client_factory


@pytest.mark.asyncio
async def test_closing_http_client_factory():
    async with closing_http_client_factory(
            base_url='http://localhost:8000',
    ) as actual_http_client:

        async with httpx.AsyncClient(
                base_url='http://localhost:8000',
        ) as expected_http_client:

            assert actual_http_client.base_url == expected_http_client.base_url
