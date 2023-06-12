from collections.abc import Iterable
from typing import TypeAlias

from dodo_is_api import models as dodo_is_api_models

import models.report_views as view_models
from services.converters import UnitsConverter

__all__ = ('calculate_tracking_pending_and_cooking_time',)

UnitsOrdersHandoverStatistics: TypeAlias = (
    Iterable[dodo_is_api_models.UnitOrdersHandoverStatistics]
)


def calculate_tracking_pending_and_cooking_time(
        unit_names: Iterable[str],
        units_statistics: UnitsOrdersHandoverStatistics,
) -> list[view_models.UnitRestaurantCookingTimeStatisticsViewDTO]:
    unit_name_to_statistics = {
        unit_statistics.unit_name: (
                unit_statistics.average_tracking_pending_time
                + unit_statistics.average_cooking_time
        )
        for unit_statistics in units_statistics
    }

    units_cooking_time = []
    for unit_name in unit_names:
        average_cooking_time = unit_name_to_statistics.get(unit_name, 0)
        units_cooking_time.append(
            view_models.UnitRestaurantCookingTimeStatisticsViewDTO(
                unit_name=unit_name,
                average_tracking_pending_and_cooking_time=average_cooking_time,
            )
        )

    return units_cooking_time
