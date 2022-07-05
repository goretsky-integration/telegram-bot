import logging

from config import app_settings

__all__ = (
    'logger',
)

log_level = logging.DEBUG if app_settings.debug else logging.INFO
logging.basicConfig(encoding='utf-8', level=logging.DEBUG)
logger = logging.getLogger()
