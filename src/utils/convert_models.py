from typing import Iterable, TypedDict
from dataclasses import dataclass

import models

__all__ = (
    'UnitsConverter',
)


@dataclass(slots=True, frozen=True)
class UnitsConverter:
    units: Iterable[models.Unit]

    @property
    def ids(self) -> list[int]:
        return [unit.id for unit in self.units]

    @property
    def id_to_name(self) -> dict[int, str]:
        return {unit.id: unit.name for unit in self.units}

    @property
    def name_to_id(self) -> dict[str, int]:
        return {unit.name: unit.id for unit in self.units}

    @property
    def ids_and_names(self) -> list[models.UnitIdAndName]:
        return [unit.dict(include={'id', 'name'}) for unit in self.units]
