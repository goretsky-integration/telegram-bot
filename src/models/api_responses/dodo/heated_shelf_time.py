from uuid import UUID

from pydantic import BaseModel

__all__ = ('UnitHeatedShelfTimeStatisticsReport',)


class UnitHeatedShelfTimeStatisticsReport(BaseModel):
    unit_uuid: UUID
    average_heated_shelf_time: int
