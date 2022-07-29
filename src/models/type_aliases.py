from typing import TypeAlias, TypedDict

__all__ = (
    'Cookies',
)

Cookies: TypeAlias = dict[str, str]


class UnitIdAndName(TypedDict):
    id: int
    name: str
