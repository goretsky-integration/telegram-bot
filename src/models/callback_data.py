from typing import TypedDict

__all__ = (
    'ReportTypeCallbackData',
    'StatisticsReportTypeCallbackData',
    'UnitsByRegionCallbackData',
    'SwitchUnitStatusCallbackData',
)


class ReportTypeCallbackData(TypedDict):
    name: str


class StatisticsReportTypeCallbackData(TypedDict):
    name: str


class UnitsByRegionCallbackData(TypedDict):
    region_id: str
    report_type: str


class SwitchUnitStatusCallbackData(TypedDict):
    report_type: str
    is_unit_enabled: str
    unit_id: str
    region_id: str
