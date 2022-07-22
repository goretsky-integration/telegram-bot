import pytest

from utils.exceptions import raise_on_none


@raise_on_none(ValueError)
def get_none_sync(value):
    return value


@raise_on_none(ValueError)
async def get_none_async(value):
    return value


def test_function_raises_error_on_none():
    with pytest.raises(ValueError):
        get_none_sync(None)


@pytest.mark.asyncio
async def test_coroutine_raises_error_on_none():
    with pytest.raises(ValueError):
        await get_none_async(None)


@pytest.mark.parametrize(
    'value',
    [
        'Rustam',
        123,
        [],
        tuple(),
        set(),
        {},
    ]
)
def test_function_does_not_raise_error(value):
    assert get_none_sync(value) is not None


@pytest.mark.asyncio
@pytest.mark.parametrize(
    'value',
    [
        'Rustam',
        123,
        [],
        tuple(),
        set(),
        {},
    ]
)
async def test_function_does_not_raise_error_async(value):
    assert await get_none_async(value) is not None


