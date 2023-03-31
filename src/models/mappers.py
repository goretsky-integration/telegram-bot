from dataclasses import dataclass

from models.api_responses import database as models


__all__ = ('RegionUnits',)


@dataclass(frozen=True, slots=True)
class RegionUnits:
    region: models.Region
    units: list[models.Unit]
