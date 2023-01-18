from aiogram import Dispatcher

from . import (
    total_cooking_time,
    restaurant_cooking_time,
    kitchen_productivity,
    heated_shelf_time,
    delivery_speed,
    delivery_productivity,
    being_late_certificates,
    revenue,
    awaiting_orders,
    bonus_system,
    productivity_balance,
)

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher):
    modules = (
        total_cooking_time,
        restaurant_cooking_time,
        kitchen_productivity,
        heated_shelf_time,
        delivery_speed,
        delivery_productivity,
        being_late_certificates,
        revenue,
        awaiting_orders,
        bonus_system,
        productivity_balance,
    )
    for module in modules:
        module.register_handlers(dispatcher)
