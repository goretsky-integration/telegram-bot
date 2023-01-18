from pydantic import BaseModel

__all__ = ('UnitKitchenProductivityStatistics', 'KitchenProductivityStatisticsReport')


class UnitKitchenProductivityStatistics(BaseModel):
    unit_id: int
    sales_per_labor_hour_today: int
    from_week_before_percent: int
    total_cooking_time: int


class KitchenProductivityStatisticsReport(BaseModel):
    results: tuple[UnitKitchenProductivityStatistics, ...]
    errors: tuple[int, ...]
