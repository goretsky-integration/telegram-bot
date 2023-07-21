from aiogram import Dispatcher

from . import (
    cooking_time,
    kitchen_productivity,
    heated_shelf_time,
    delivery_speed,
    delivery_productivity,
    being_late_certificates,
    revenue,
    awaiting_orders,
    bonus_system,
    productivity_balance,
    restaurant_cooking_time,
)

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher):
    modules = (
        cooking_time,
        kitchen_productivity,
        heated_shelf_time,
        delivery_speed,
        delivery_productivity,
        being_late_certificates,
        revenue,
        awaiting_orders,
        bonus_system,
        productivity_balance,
        restaurant_cooking_time,
    )
    for module in modules:
        module.register_handlers(dispatcher)
