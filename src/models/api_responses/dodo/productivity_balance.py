from uuid import UUID

from pydantic import BaseModel

__all__ = ('UnitProductivityBalanceStatisticsReport',)


class UnitProductivityBalanceStatisticsReport(BaseModel):
    unit_uuid: UUID
    sales_per_labor_hour: int
    orders_per_labor_hour: int
    stop_sale_duration_in_seconds: int
