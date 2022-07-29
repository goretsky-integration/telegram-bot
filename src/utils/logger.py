from loguru import logger

from config import app_settings, LOG_FILE_PATH

__all__ = (
    'logger',
)

log_level = 'DEBUG' if app_settings.debug else 'INFO'
logger.add(LOG_FILE_PATH, encoding='utf-8', level=log_level)
