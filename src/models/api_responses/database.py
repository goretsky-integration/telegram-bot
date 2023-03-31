from uuid import UUID

from pydantic import BaseModel

__all__ = (
    'Unit',
    'Region',
    'ReportRoute',
    'ReportType',
)


class Region(BaseModel):
    id: int
    name: str


class Unit(BaseModel):
    id: int
    name: str
    uuid: UUID
    region_id: int


class ReportRoute(BaseModel):
    report_type: str
    chat_id: int
    unit_ids: set[int]


class ReportType(BaseModel):
    id: int
    name: str
    verbose_name: str
