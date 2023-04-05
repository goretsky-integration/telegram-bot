from dataclasses import dataclass

from models.api_responses import database as models

__all__ = ('RegionUnits', 'ChatToCreate')


@dataclass(frozen=True, slots=True)
class ChatToCreate:
    id: int
    type: str
    username: str | None
    title: str


@dataclass(frozen=True, slots=True)
class RegionUnits:
    region: models.Region
    units: list[models.Unit]
