import asyncio
from typing import TypeVar, Iterable, Collection

from aiogram.types import Message, CallbackQuery, Update

import models.api_responses.database as database_models
from core import exceptions
from views.base import BaseView

__all__ = (
    'answer_views',
    'flatten',
    'get_message',
    'validate_report_routes',
    'filter_units_by_ids',
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


def validate_report_routes(reports: Collection[database_models.ReportRoute]):
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


def filter_units_by_ids(
        units: Iterable[database_models.Unit],
        allowed_unit_ids: Iterable[int],
) -> list[database_models.Unit]:
    allowed_unit_ids = set(allowed_unit_ids)
    return [unit for unit in units if unit.id in allowed_unit_ids]
