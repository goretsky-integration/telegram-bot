import asyncio
from typing import TypeVar, Iterable

from aiogram.types import Message, CallbackQuery, Update

import models.api_responses.database as database_models
from views.base import BaseView

__all__ = (
    'answer_views',
    'flatten',
    'get_message',
    'filter_units_by_ids',
    'edit_message_by_view',
)

T = TypeVar('T')


async def answer_views(message: Message, *views: BaseView, edit: bool = False):
    method = message.edit_text if edit else message.answer
    for view in views:
        await method(view.get_text(), reply_markup=view.get_reply_markup())
        await asyncio.sleep(0.1)


async def edit_message_by_view(message: Message, view: BaseView) -> Message:
    return await message.edit_text(text=view.get_text(), reply_markup=view.get_reply_markup())


def flatten(nested: Iterable[Iterable[T]]) -> list[T]:
    return [item for items in nested
            for item in items]


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
