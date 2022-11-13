from loguru import logger

from config import get_app_settings, LOG_FILE_PATH

__all__ = (
    'logger',
)

log_level = 'DEBUG' if get_app_settings().debug else 'INFO'
logger.add(LOG_FILE_PATH, encoding='utf-8', level=log_level)
