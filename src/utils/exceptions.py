"""
- DatabaseAPIError
    - AuthCredentialsAPIError
        - NoCookiesError
        - NoTokenError
- DodoAPIError
"""


class DodoAPIError(Exception):
    pass


class DatabaseAPIError(Exception):
    pass


class AuthCredentialsAPIError(DatabaseAPIError):
    pass


class NoCookiesError(AuthCredentialsAPIError):
    pass


class NoTokenError(AuthCredentialsAPIError):
    pass
