from pydantic import BaseModel

__all__ = ('UnitTripsWithOneOrderStatisticsReport',)


class UnitTripsWithOneOrderStatisticsReport(BaseModel):
    unit_name: str
    percentage: float
