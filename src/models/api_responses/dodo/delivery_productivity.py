from uuid import UUID

from pydantic import BaseModel

__all__ = ('UnitDeliveryProductivityStatisticsReport',)


class UnitDeliveryProductivityStatisticsReport(BaseModel):
    unit_uuid: UUID
    orders_per_courier_labour_hour_today: int
    orders_per_courier_labour_hour_week_before: int
    from_week_before_in_percents: int
