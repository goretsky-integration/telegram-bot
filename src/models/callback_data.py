from typing import TypedDict, Literal

__all__ = (
    'ReportTypeCallbackData',
    'StatisticsReportTypeCallbackData',
    'UnitsByRegionCallbackData',
    'SwitchUnitStatusCallbackData',
    'AllUnitIdsByRegionCallbackData',
)


class ReportTypeCallbackData(TypedDict):
    report_type_id: int


class StatisticsReportTypeCallbackData(TypedDict):
    report_type_name: str


class UnitsByRegionCallbackData(TypedDict):
    region_id: int
    report_type_id: int


class SwitchUnitStatusCallbackData(TypedDict):
    report_type_id: int
    is_unit_enabled: bool
    unit_id: int
    region_id: int


class AllUnitIdsByRegionCallbackData(TypedDict):
    region_id: int
    report_type_id: int
    action: Literal['disable', 'enable']
