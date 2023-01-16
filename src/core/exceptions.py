class ApplicationError(Exception):
    """Base exception class for the whole app."""


class APIServiceError(Exception):
    pass


class JSONDecodeError(APIServiceError):
    pass


class DatabaseAPIServiceError(APIServiceError):
    pass


class DodoAPIServiceError(APIServiceError):
    pass
