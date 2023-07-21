from bs4 import BeautifulSoup

from models.api_responses import UnitRestaurantCookingTimeStatisticsReport

__all__ = ('parse_kitchen_partial_statistics_html',)


def parse_kitchen_partial_statistics_html(
        *,
        unit_id: int,
        html: str,
) -> UnitRestaurantCookingTimeStatisticsReport:
    soup = BeautifulSoup(html, 'lxml')
    h1 = soup.find_all(attrs={'class': 'operationalStatistics_panelTitle'})[2]
    minutes, seconds = h1.text.strip().split(':')
    return UnitRestaurantCookingTimeStatisticsReport(
        unit_id=unit_id,
        minutes=minutes,
        seconds=seconds,
    )
