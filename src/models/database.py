import uuid
from dataclasses import dataclass
from enum import Enum

__all__ = (
    'ReportType',
    'Region',
    'Unit',
    'StatisticsReportType',
)

from pydantic import BaseModel


class ReportType(Enum):
    STATISTICS = 'Отчёты по статистике'
    INGREDIENTS_STOP_SALES = 'Стопы (Ингредиент)'
    STREET_STOP_SALES = 'Стопы (Улица)'
    SECTOR_STOP_SALES = 'Стопы (Сектор)'
    PIZZERIA_STOP_SALES = 'Стопы (Пиццерия)'
    STOPS_AND_RESUMES = 'Стопы-возобновления'
    CANCELED_ORDERS = 'Отмены заказов'
    CHEATED_PHONE_NUMBERS = 'Мошенничество с номерами'


class StatisticsReportType(Enum):
    COOKING_TIME = 'Время приготовления'
    KITCHEN_PERFORMANCE = 'Производительность кухни'
    DELIVERY_AWAITING_TIME = 'Время на полке'
    DELIVERY_SPEED = 'Скорость доставки'
    DELIVERY_PERFORMANCE = 'Производительность доставки'
    BEING_LATE_CERTIFICATES = 'Сертификаты за опоздание'
    DAILY_REVENUE = 'Выручка за сегодня'
    AWAITING_ORDERS = 'Остывает на полке'
    BONUS_SYSTEM = 'Бонусная система'


@dataclass(frozen=True, slots=True)
class Region:
    id: int
    name: str


class Unit(BaseModel):
    id: int
    name: str
    uuid: uuid.UUID
