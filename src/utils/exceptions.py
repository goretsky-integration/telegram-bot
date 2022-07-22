import asyncio
from typing import Type, Iterable, Any


class DodoAPIError(Exception):
    pass


class NoneUnitIdsSetUpError(Exception):
    pass


class NoCookiesError(Exception):
    pass


class NoTokenError(Exception):
    pass


def raise_on_none(exception: Type[Exception], *exception_args: Iterable[Any]):
    def wrapper(func):
        if asyncio.iscoroutinefunction(func):
            async def inner(*args, **kwargs):
                response = await func(*args, **kwargs)
                if response is None:
                    raise exception(*exception_args)
                return response
        else:
            def inner(*args, **kwargs):
                response = func(*args, **kwargs)
                if response is None:
                    raise exception(*exception_args)
                return response
        return inner
    return wrapper
