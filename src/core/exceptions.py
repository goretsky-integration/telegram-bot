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


class AuthAPIServiceError(APIServiceError):

    def __init__(self, *, account_name: str):
        exception_message = f'Could not retrieve auth credentials for account "{account_name}"'
        super().__init__(exception_message)
        self.account_name = account_name


class NoEnabledUnitsError(ApplicationError):
    pass


class UserHasNoRoleError(DatabaseAPIServiceError):
    pass


class RoleNotFoundError(DatabaseAPIServiceError):
    pass


class UserNotFoundError(DatabaseAPIServiceError):

    def __init__(self, *args, chat_id: int):
        super().__init__(*args)
        self.chat_id = chat_id


class UserAlreadyExistsError(DatabaseAPIServiceError):
    pass
