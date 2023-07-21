from pydantic import BaseModel

__all__ = ('UnitRestaurantCookingTimeStatisticsReport',)


class UnitRestaurantCookingTimeStatisticsReport(BaseModel):
    unit_id: int
    minutes: int
    seconds: int
