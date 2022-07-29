from typing import TypedDict, Literal

__all__ = (
    'ReportTypeCallbackData',
    'StatisticsReportTypeCallbackData',
    'UnitsByRegionCallbackData',
    'SwitchUnitStatusCallbackData',
    'AllUnitIdsByRegionCallbackData',
)


class ReportTypeCallbackData(TypedDict):
    report_type_name: str


class StatisticsReportTypeCallbackData(TypedDict):
    report_type_name: str


class UnitsByRegionCallbackData(TypedDict):
    region: str
    report_type_name: str


class SwitchUnitStatusCallbackData(TypedDict):
    report_type: str
    is_unit_enabled: str
    unit_id: str
    region: str


class AllUnitIdsByRegionCallbackData(TypedDict):
    region: str
    report_type: str
    action: Literal['disable', 'enable']
