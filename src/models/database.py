import uuid
from enum import Enum

__all__ = (
    'ReportType',
    'Unit',
    'StatisticsReportType',
)

from pydantic import BaseModel


class ReportType(Enum):
    STATISTICS = 'Отчёты по статистике'
    INGREDIENTS_STOP_SALES = 'Стопы (тесто, сыр, пицца-соус)'
    STREET_STOP_SALES = 'Стопы (Улица)'
    SECTOR_STOP_SALES = 'Стопы (Сектор)'
    PIZZERIA_STOP_SALES = 'Стопы (Пиццерия)'
    STOPS_AND_RESUMES = 'Стопы (Остальные ингредиенты)'
    CANCELED_ORDERS = 'Отмены заказов'
    CHEATED_PHONE_NUMBERS = 'Мошенничество с номерами'


class StatisticsReportType(Enum):
    COOKING_TIME = 'Время приготовления (общее)'
    RESTAURANT_COOKING_TIME = 'Время приготовления (ресторан)'
    KITCHEN_PERFORMANCE = 'Производительность кухни'
    DELIVERY_AWAITING_TIME = 'Время на полке'
    DELIVERY_SPEED = 'Скорость доставки'
    DELIVERY_PERFORMANCE = 'Производительность доставки'
    BEING_LATE_CERTIFICATES = 'Сертификаты за опоздание'
    DAILY_REVENUE = 'Выручка за сегодня'
    AWAITING_ORDERS = 'Остывает на полке'
    BONUS_SYSTEM = 'Бонусная система'


class Unit(BaseModel):
    id: int
    name: str
    uuid: uuid.UUID
    account_name: str
    region: str
