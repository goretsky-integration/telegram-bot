import models.report_views as view_models
import models.api_responses.dodo as api_models

__all__ = (
    'to_revenue_statistics_view_dto',
)


def to_revenue_statistics_view_dto(
        revenue_statistics: api_models.RevenueStatisticsReport,
        unit_id_to_name: dict[int, str],
) -> view_models.RevenueStatisticsReportViewDTO:
    return view_models.RevenueStatisticsReportViewDTO(
        units=[
            view_models.UnitRevenueStatisticsDTO(
                unit_name=unit_id_to_name[unit.unit_id],
                revenue_today=unit.today,
                from_week_before_in_percents=unit.from_week_before_in_percents,
            ) for unit in revenue_statistics.results.units
        ],
        total=view_models.TotalRevenueStatisticsDTO(
            revenue_today=revenue_statistics.results.total.today,
            from_week_before_in_percents=revenue_statistics.results.total.from_week_before_in_percents,
        ),
        error_unit_names=[unit_id_to_name[unit_id] for unit_id in revenue_statistics.errors]
    )
