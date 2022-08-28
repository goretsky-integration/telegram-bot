import functools
from typing import TypedDict, Callable, Awaitable, Type

from dodolib import DodoAPIClient
from dodolib.models import (
    SalesChannel,
    OrdersHandoverTimeStatistics,
    KitchenPerformanceStatistics,
    KitchenProductionStatistics,
    DeliveryPerformanceStatistics,
    BonusSystemStatistics,
    BeingLateCertificatesStatistics,
    DeliverySpeedStatistics,
    HeatedShelfStatistics,
)
from pydantic import BaseModel

import responses
from responses.base import Response
from utils import constants

__all__ = (
    'STATISTICS_REPORT_TYPE_TO_STRATEGY',
)


class Strategy(TypedDict):
    method: Callable[..., Awaitable]
    model: Type[BaseModel]
    response: Type[Response]


STATISTICS_REPORT_TYPE_TO_STRATEGY: dict[str, Strategy] = {
    constants.StatisticsReportType.KITCHEN_PERFORMANCE.name: {
        'method': DodoAPIClient.get_kitchen_performance_statistics,
        'model': KitchenPerformanceStatistics,
        'response': responses.KitchenPerformanceStatistics,
    },
    constants.StatisticsReportType.DELIVERY_PERFORMANCE.name: {
        'method': DodoAPIClient.get_delivery_performance_statistics,
        'model': DeliveryPerformanceStatistics,
        'response': responses.DeliveryPerformanceStatistics,
    },
    constants.StatisticsReportType.COOKING_TIME.name: {
        'method': DodoAPIClient.get_kitchen_production_statistics,
        'model': KitchenProductionStatistics,
        'response': responses.TotalCookingTimeStatistics,
    },
    constants.StatisticsReportType.DELIVERY_AWAITING_TIME.name: {
        'method': DodoAPIClient.get_heated_shelf_time_statistics,
        'model': HeatedShelfStatistics,
        'response': responses.HeatedShelfTimeStatistics,
    },
    constants.StatisticsReportType.DELIVERY_SPEED.name: {
        'method': DodoAPIClient.get_delivery_speed_statistics,
        'model': DeliverySpeedStatistics,
        'response': responses.DeliverySpeedStatistics,
    },
    constants.StatisticsReportType.RESTAURANT_COOKING_TIME.name: {
        'method': functools.partial(DodoAPIClient.get_orders_handover_time_statistics,
                                    sales_channels=[SalesChannel.DINE_IN]),
        'model': OrdersHandoverTimeStatistics,
        'response': responses.RestaurantCookingTime,
    },
    constants.StatisticsReportType.BEING_LATE_CERTIFICATES.name: {
        'method': DodoAPIClient.get_being_late_certificates_statistics,
        'model': BeingLateCertificatesStatistics,
        'response': responses.BeingLateCertificatesStatistics,
    },
    constants.StatisticsReportType.BONUS_SYSTEM.name: {
        'method': DodoAPIClient.get_bonus_system_statistics,
        'model': BonusSystemStatistics,
        'response': responses.BonusSystemStatistics,
    },
}
