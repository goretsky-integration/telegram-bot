from typing import TypeAlias, TypedDict

from aiogram.types import Message, CallbackQuery, Update

__all__ = (
    'Cookies',
    'UnitIdAndName',
    'Query',
)

Cookies: TypeAlias = dict[str, str]
Query: TypeAlias = Message | CallbackQuery | Update


class UnitIdAndName(TypedDict):
    id: int
    name: str
