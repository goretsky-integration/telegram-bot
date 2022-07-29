"""
- DatabaseAPIError
    - AuthCredentialsAPIError
        - NoCookiesError
        - NoTokenError
- DodoAPIError
    - DodoAPIRequestByUnitIdsError
    - DodoAPIRequestByUnitUUIDsError
    - DodoAPIRequestByUnitIdsAndNamesError
"""
from typing import Iterable
from uuid import UUID

import models


class DodoAPIError(Exception):
    pass


class DodoAPIRequestByUnitIdsError(DodoAPIError):

    def __init__(self, *args, unit_ids: Iterable[int]):
        super().__init__(*args)
        self.unit_ids = tuple(unit_ids)


class DodoAPIRequestByUnitUUIDsError(DodoAPIError):

    def __init__(self, *args, unit_uuids: Iterable[UUID]):
        super().__init__(*args)
        self.unit_uuids = tuple(unit_uuids)


class DodoAPIRequestByUnitIdsAndNamesError(DodoAPIError):
    def __init__(self, *args, unit_ids_and_names: Iterable[models.UnitIdAndName]):
        super().__init__(*args)
        self.unit_ids_and_names = tuple(unit_ids_and_names)


class DatabaseAPIError(Exception):
    pass


class AuthCredentialsAPIError(DatabaseAPIError):

    def __init__(self, *args, account_name: str):
        super().__init__(*args)
        self.account_name = account_name


class NoCookiesError(AuthCredentialsAPIError):
    pass


class NoTokenError(AuthCredentialsAPIError):
    pass
