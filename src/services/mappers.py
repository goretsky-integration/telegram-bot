from collections import defaultdict
from collections.abc import Iterable

from models.api_responses import database as models
from models.mappers import RegionUnits


def group_units_by_region(
        *,
        units: Iterable[models.Unit],
        regions: Iterable[models.Region],
) -> list[RegionUnits]:
    region_id_to_units: defaultdict[int, list[models.Unit]] = defaultdict(list)
    for unit in units:
        region_id_to_units[unit.region_id].append(unit)
    return [
        RegionUnits(
            region=region,
            units=region_id_to_units[region.id],
        ) for region in regions
    ]
