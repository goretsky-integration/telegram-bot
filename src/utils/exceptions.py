"""
- DatabaseAPIError
    - NoCookiesError
    - NoTokenError
"""


class DodoAPIError(Exception):
    pass


class DatabaseAPIError(Exception):
    pass


class NoneUnitIdsSetUpError(Exception):
    pass


class NoCookiesError(DatabaseAPIError):
    pass


class NoTokenError(DatabaseAPIError):
    pass
