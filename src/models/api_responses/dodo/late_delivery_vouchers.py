from uuid import UUID

from pydantic import BaseModel

__all__ = ('UnitLateDeliveryVouchersStatisticsReport',)


class UnitLateDeliveryVouchersStatisticsReport(BaseModel):
    unit_uuid: UUID
    certificates_count_today: int
    certificates_count_week_before: int
