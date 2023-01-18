from uuid import UUID

from pydantic import BaseModel

__all__ = ('UnitRestaurantCookingTimeStatisticsReport',)


class UnitRestaurantCookingTimeStatisticsReport(BaseModel):
    unit_uuid: UUID
    average_tracking_pending_and_cooking_time: int
