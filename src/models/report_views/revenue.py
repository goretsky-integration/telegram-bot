from dataclasses import dataclass

__all__ = (
    'UnitRevenueStatisticsDTO',
    'TotalRevenueStatisticsDTO',
    'RevenueStatisticsReportViewDTO',
)


@dataclass(frozen=True, slots=True)
class UnitRevenueStatisticsDTO:
    unit_name: str
    revenue_today: int
    from_week_before_in_percents: int


@dataclass(frozen=True, slots=True)
class TotalRevenueStatisticsDTO:
    revenue_today: int
    from_week_before_in_percents: int


@dataclass(frozen=True, slots=True)
class RevenueStatisticsReportViewDTO:
    units: list[UnitRevenueStatisticsDTO]
    total: TotalRevenueStatisticsDTO
    error_unit_names: list[str]
