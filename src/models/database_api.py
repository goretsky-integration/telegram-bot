import uuid

from pydantic import BaseModel

from models.type_aliases import Cookies

__all__ = (
    'ReportType',
    'Unit',
    'StatisticsReportType',
    'AuthToken',
    'AuthCookies',
    'Report',
)


class Unit(BaseModel):
    id: int
    name: str
    uuid: uuid.UUID
    account_name: str
    region: str


class AuthCookies(BaseModel):
    account_name: str
    cookies: Cookies


class AuthToken(BaseModel):
    account_name: str
    access_token: str


class ReportType(BaseModel):
    id: int
    name: str
    verbose_name: str


class StatisticsReportType(BaseModel):
    id: int
    name: str
    verbose_name: str


class Report(BaseModel):
    unit_ids: list[int]
    report_type: str
    chat_id: int
