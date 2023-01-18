from pydantic import BaseModel

__all__ = ('UnitAwaitingOrdersStatistics', 'AwaitingOrdersStatisticsReport')


class UnitAwaitingOrdersStatistics(BaseModel):
    unit_id: int
    heated_shelf_orders_count: int
    couriers_in_queue_count: int
    couriers_on_shift_count: int


class AwaitingOrdersStatisticsReport(BaseModel):
    results: tuple[UnitAwaitingOrdersStatistics, ...]
    errors: tuple[int, ...]
