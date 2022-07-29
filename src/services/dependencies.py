from config import app_settings
from repositories import DatabaseRepository, AuthCredentialsRepository, DodoAPIRepository

__all__ = (
    'get_db_client',
    'get_auth_client',
    'get_dodo_api_client',
)


def get_db_client() -> DatabaseRepository:
    return DatabaseRepository(app_settings.db_api_url)


def get_auth_client() -> AuthCredentialsRepository:
    return AuthCredentialsRepository(app_settings.db_api_url)


def get_dodo_api_client() -> DodoAPIRepository:
    return DodoAPIRepository(app_settings.api_url)
