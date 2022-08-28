from dodolib import AuthClient, DatabaseClient, DodoAPIClient

from config import app_settings

__all__ = (
    'get_db_client',
    'get_auth_client',
    'get_dodo_api_client',
)


def get_db_client() -> DatabaseClient:
    return DatabaseClient(app_settings.db_api_url)


def get_auth_client() -> AuthClient:
    return AuthClient(app_settings.db_api_url)


def get_dodo_api_client() -> DodoAPIClient:
    return DodoAPIClient(app_settings.api_url)
