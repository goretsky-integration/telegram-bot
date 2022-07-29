from typing import TypeAlias, TypedDict

__all__ = (
    'Cookies',
    'UnitIdAndName',
)

Cookies: TypeAlias = dict[str, str]


class UnitIdAndName(TypedDict):
    id: int
    name: str
