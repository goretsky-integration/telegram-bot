from collections.abc import Mapping

from models.api_responses import UnitRestaurantCookingTimeStatisticsReport
from models.report_views import UnitCookingTimeStatisticsViewDTO

__all__ = ('calculate_restaurant_average_pending_and_cooking_time',)


def calculate_restaurant_average_pending_and_cooking_time(
        *,
        unit_id_to_name: Mapping[int, str],
        report: UnitRestaurantCookingTimeStatisticsReport,
) -> UnitCookingTimeStatisticsViewDTO:
    cooking_time = report.minutes * 60 + report.seconds
    return UnitCookingTimeStatisticsViewDTO(
        unit_name=unit_id_to_name[report.unit_id],
        average_tracking_pending_and_cooking_time=cooking_time,
    )
