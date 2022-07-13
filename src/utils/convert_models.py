import collections
import uuid
from dataclasses import dataclass
from typing import Iterable, TypeVar

import models

__all__ = (
    'UnitsConverter',
    'to_heated_shelf_orders_and_couriers_statistics',
)

M = TypeVar('M')


@dataclass(slots=True, frozen=True)
class UnitsConverter:
    units: Iterable[models.Unit]

    @staticmethod
    def units_to_uuids(units: Iterable[models.Unit]) -> list[uuid.UUID]:
        return [unit.uuid for unit in units]

    @staticmethod
    def units_to_ids_and_names(units: Iterable[models.Unit]) -> list[models.UnitIdAndName]:
        return [unit.dict(include={'id', 'name'}) for unit in units]

    @staticmethod
    def units_to_ids(units: Iterable[models.Unit]) -> list[int]:
        return [unit.id for unit in units]

    @property
    def ids(self) -> list[int]:
        return self.units_to_ids(self.units)

    @property
    def id_to_name(self) -> dict[int, str]:
        return {unit.id: unit.name for unit in self.units}

    @property
    def name_to_id(self) -> dict[str, int]:
        return {unit.name: unit.id for unit in self.units}

    @property
    def ids_and_names(self) -> list[models.UnitIdAndName]:
        return self.units_to_ids_and_names(self.units)

    @property
    def account_names_to_units(self) -> dict[str, list[models.Unit]]:
        account_name_to_units: dict[str, list[models.Unit]] = collections.defaultdict(list)
        for unit in self.units:
            grouped_units: list[models.Unit] = account_name_to_units[unit.account_name]
            grouped_units.append(unit)
        return account_name_to_units

    @property
    def account_names_to_unit_ids(self) -> dict[str, list[int]]:
        return {account_name: self.units_to_ids(units)
                for account_name, units in self.account_names_to_units.items()}

    @property
    def account_names_to_unit_ids_and_names(self) -> dict[str, list[models.UnitIdAndName]]:
        return {account_name: self.units_to_ids_and_names(units)
                for account_name, units in self.account_names_to_units.items()}

    @property
    def account_names_to_unit_uuids(self) -> dict[str, list[uuid.UUID]]:
        return {account_name: self.units_to_uuids(units)
                for account_name, units in self.account_names_to_units.items()}


def unit_id_to_model(models_collection: Iterable[M]) -> dict[int, M]:
    return {model.unit_id: model for model in models_collection}


def to_heated_shelf_orders_and_couriers_statistics(
        heated_shelf_statistics: models.HeatedShelfStatistics,
        couriers_statistics: models.CouriersStatistics,
) -> models.HeatedShelfOrdersAndCouriersStatistics:
    unit_id_to_heated_shelf_statistics = unit_id_to_model(heated_shelf_statistics.units)
    unit_id_to_couriers_statistics = unit_id_to_model(couriers_statistics.units)

    statistics_unit_ids = set(unit_id_to_heated_shelf_statistics) | set(unit_id_to_couriers_statistics)
    error_unit_ids = set(heated_shelf_statistics.error_unit_ids) | set(couriers_statistics.error_unit_ids)
    success_unit_ids = statistics_unit_ids - error_unit_ids

    units_statistics = []
    for unit_id in success_unit_ids:
        unit_heated_shelf = unit_id_to_heated_shelf_statistics[unit_id]
        unit_couriers = unit_id_to_couriers_statistics[unit_id]
        units_statistics.append(models.UnitHeatedShelfOrdersAndCouriers(
            unit_id=unit_id,
            awaiting_orders_count=unit_heated_shelf.awaiting_orders_count,
            in_queue_count=unit_couriers.in_queue_count,
            total_count=unit_couriers.total_count,
        ))
    return models.HeatedShelfOrdersAndCouriersStatistics(units=units_statistics, error_unit_ids=error_unit_ids)
