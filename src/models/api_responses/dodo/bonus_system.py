from pydantic import BaseModel

__all__ = ('UnitBonusSystemStatisticsReport',)


class UnitBonusSystemStatisticsReport(BaseModel):
    unit_id: int
    orders_with_phone_numbers_count: int
    orders_with_phone_numbers_percent: int
    total_orders_count: int
