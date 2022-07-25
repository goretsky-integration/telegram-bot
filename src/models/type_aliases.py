from typing import TypeAlias

__all__ = (
    'SerializedJSON',
    'Cookies',
    'AccessToken',
)

SerializedJSON: TypeAlias = dict | list
Cookies: TypeAlias = dict[str, str]
AccessToken: TypeAlias = str
