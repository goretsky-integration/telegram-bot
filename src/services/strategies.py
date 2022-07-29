from typing import TypedDict, Callable, Awaitable, Type

from pydantic import BaseModel

import models
import responses
from utils import constants
from responses.base import Response
from repositories import DodoAPIRepository

__all__ = (
    'STATISTICS_REPORT_TYPE_TO_STRATEGY',
)


class Strategy(TypedDict):
    method: Callable[..., Awaitable]
    model: Type[BaseModel]
    response: Type[Response]


STATISTICS_REPORT_TYPE_TO_STRATEGY: dict[str, Strategy] = {
    constants.StatisticsReportType.KITCHEN_PERFORMANCE.name: {
        'method': DodoAPIRepository.get_kitchen_performance_statistics,
        'model': models.KitchenPerformanceStatistics,
        'response': responses.KitchenPerformanceStatistics,
    },
    constants.StatisticsReportType.DELIVERY_PERFORMANCE.name: {
        'method': DodoAPIRepository.get_delivery_performance_statistics,
        'model': models.DeliveryPerformanceStatistics,
        'response': responses.DeliveryPerformanceStatistics,
    },
    constants.StatisticsReportType.COOKING_TIME.name: {
        'method': DodoAPIRepository.get_kitchen_production_statistics,
        'model': models.KitchenProductionStatistics,
        'response': responses.TotalCookingTimeStatistics,
    },
    constants.StatisticsReportType.DELIVERY_AWAITING_TIME.name: {
        'method': DodoAPIRepository.get_heated_shelf_statistics,
        'model': models.HeatedShelfStatistics,
        'response': responses.HeatedShelfTimeStatistics,
    },
    constants.StatisticsReportType.DELIVERY_SPEED.name: {
        'method': DodoAPIRepository.get_delivery_speed_statistics,
        'model': models.DeliverySpeedStatistics,
        'response': responses.DeliverySpeedStatistics,
    },
    constants.StatisticsReportType.RESTAURANT_COOKING_TIME.name: {
        'method': DodoAPIRepository.get_orders_handover_time_statistics,
        'model': models.OrdersHandoverTimeStatistics,
        'response': responses.RestaurantCookingTime,
    },
    constants.StatisticsReportType.BEING_LATE_CERTIFICATES.name: {
        'method': DodoAPIRepository.get_being_late_certificates_statistics,
        'model': models.BeingLateCertificatesStatistics,
        'response': responses.BeingLateCertificatesStatistics,
    },
    constants.StatisticsReportType.BONUS_SYSTEM.name: {
        'method': DodoAPIRepository.get_bonus_system_statistics,
        'model': models.BonusSystemStatistics,
        'response': responses.BonusSystemStatistics,
    },
}
