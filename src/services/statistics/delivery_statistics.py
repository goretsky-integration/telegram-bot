import asyncio
import itertools
from typing import Iterable

import db
import models
import utils.helpers
from services import api


async def get_delivery_statistics(units: Iterable[models.Unit]) -> tuple[models.UnitDeliveryStatistics, ...]:
    account_name_to_units = utils.helpers.group_units_by_account_name(units)
    tasks = []
    for account_name, units in account_name_to_units.items():
        unit_uuids = [unit.uuid for unit in units]
        token = await db.get_access_token(account_name)
        tasks.append(api.get_delivery_statistics(token, unit_uuids))
    all_units_delivery_statistics_nested = await asyncio.gather(*tasks)
    return tuple(itertools.chain.from_iterable(all_units_delivery_statistics_nested))
