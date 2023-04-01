from aiogram import Dispatcher

from . import (
    errors,
    reports,
    roles,
    start,
    settings,
)

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    errors.register_handlers(dispatcher)
    roles.register_message_handlers(dispatcher)
    start.register_handlers(dispatcher)
    settings.register_handlers(dispatcher)
    reports.register_handlers(dispatcher)
