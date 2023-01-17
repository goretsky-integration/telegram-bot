from uuid import UUID

from pydantic import BaseModel

__all__ = (
    'Unit',
    'ReportRoute',
    'ReportType',
)


class Unit(BaseModel):
    id: int
    name: str
    uuid: UUID
    region: str
    account_name: str


class ReportRoute(BaseModel):
    report_type: str
    chat_id: int
    unit_ids: set[int]


class ReportType(BaseModel):
    id: int
    name: str
    verbose_name: str
