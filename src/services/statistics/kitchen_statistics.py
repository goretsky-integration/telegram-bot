import asyncio
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
    tasks = []
    for account_name, units in account_name_to_units.items():
        unit_ids = [unit.id for unit in units]
        cookies = await db.get_cookies(account_name)
        tasks.append(api.get_kitchen_statistics(unit_ids, cookies))

    units_kitchen_statistics = await asyncio.gather(*tasks)
    all_units_kitchen_statistics = []
    kitchen_statistics_error_unit_ids = []

    for unit_kitchen_statistics in units_kitchen_statistics:
        all_units_kitchen_statistics += unit_kitchen_statistics.kitchen_statistics
        kitchen_statistics_error_unit_ids += unit_kitchen_statistics.error_unit_ids

    return models.KitchenStatisticsBatch(
        kitchen_statistics=all_units_kitchen_statistics,
        error_unit_ids=kitchen_statistics_error_unit_ids,
    )
