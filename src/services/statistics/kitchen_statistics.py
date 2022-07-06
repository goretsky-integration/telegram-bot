from typing import Iterable

import db
import models
import utils.helpers
from services import api

__all__ = (
    'get_kitchen_statistics',
)


async def get_kitchen_statistics(units: Iterable[models.Unit]) -> models.KitchenStatisticsBatch:
    account_name_to_units = utils.helpers.group_units_by_account_name(units)

    all_units_kitchen_statistics = []
    kitchen_statistics_error_unit_ids = []

    for account_name, units in account_name_to_units.items():
        unit_ids = [unit.id for unit in units]
        cookies = await db.get_cookies(account_name)
        kitchen_statistics = await api.get_kitchen_statistics(unit_ids, cookies)

        all_units_kitchen_statistics += kitchen_statistics.kitchen_statistics
        kitchen_statistics_error_unit_ids += kitchen_statistics.error_unit_ids

    return models.KitchenStatisticsBatch(
        kitchen_statistics=all_units_kitchen_statistics,
        error_unit_ids=kitchen_statistics_error_unit_ids,
    )
