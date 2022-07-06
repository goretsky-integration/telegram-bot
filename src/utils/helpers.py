import collections
from typing import Iterable

import models


def group_units_by_account_name(units: Iterable[models.Unit]) -> dict[str, list[models.Unit]]:
    account_name_to_units = collections.defaultdict(list)
    for unit in units:
        grouped_units = account_name_to_units[unit.account_name]
        grouped_units.append(unit)
    return account_name_to_units
