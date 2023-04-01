from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = ('SetUserRoleStates',)


class SetUserRoleStates(StatesGroup):
    access_code = State()
