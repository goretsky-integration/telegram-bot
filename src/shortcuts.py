import asyncio
import uuid
from typing import TypeVar, Iterable, Sequence, Callable, Awaitable

from aiogram.types import Message, CallbackQuery, Update
from dodolib import models, AuthClient

from utils import exceptions
from views.base import BaseView

__all__ = (
    'answer_views',
    'flatten',
    'get_message',
    'validate_reports',
    'get_statistics_report_by_tokens_batch',
    'get_accounts_tokens_batch',
    'filter_units_by_ids',
    'filter_exceptions',
)

T = TypeVar('T')


async def answer_views(message: Message, *views: BaseView, edit: bool = False):
    method = message.edit_text if edit else message.answer
    for view in views:
        await method(view.get_text(), reply_markup=view.get_reply_markup())
        await asyncio.sleep(0.1)


def flatten(nested: Iterable[Iterable[T]]) -> list[T]:
    return [item for items in nested
            for item in items]


def validate_reports(reports: Sequence[models.Report]):
    if not reports or not reports[0].unit_ids:
        raise exceptions.NoEnabledUnitsError


def get_message(query: Message | CallbackQuery | Update) -> Message:
    match query:
        case Message():
            return query
        case Update() if query.callback_query is not None:
            return query.callback_query.message
        case CallbackQuery() | Update() if query.message is not None:
            return query.message
        case _:
            raise ValueError('Query must be Message, CallbackQuery or Update type')


async def get_accounts_tokens_batch(
        auth_client: AuthClient,
        account_names: Iterable[str],
) -> tuple[models.AuthToken, ...]:
    tasks = (auth_client.get_tokens(account_name) for account_name in account_names)
    try:
        accounts_tokens: tuple[models.AuthToken, ...] = await asyncio.gather(*tasks)
    except Exception:
        raise exceptions.AuthAPIError
    return accounts_tokens


async def get_statistics_report_by_tokens_batch(
        api_method: Callable[..., Awaitable],
        account_name_to_unit_uuids: dict[str, Iterable[uuid.UUID]],
        accounts_tokens: Iterable[models.AuthToken]
) -> list:
    tasks = (api_method(account_tokens.access_token,
                        'ru',
                        account_name_to_unit_uuids[account_tokens.account_name])
             for account_tokens in accounts_tokens)
    units_statistics = await asyncio.gather(*tasks, return_exceptions=True)
    return flatten(filter_exceptions(units_statistics))


def filter_units_by_ids(units: Iterable[models.Unit], allowed_unit_ids: Iterable[int]) -> list[models.Unit]:
    allowed_unit_ids = set(allowed_unit_ids)
    return [unit for unit in units if unit.id in allowed_unit_ids]


def filter_exceptions(elements: Iterable[T | Exception]) -> list[T]:
    return [element for element in elements if not isinstance(element, Exception)]
