import asyncio
from typing import Iterable

import db
import models
import utils.helpers
from services import api


async def get_being_late_certificates_statistics(
        units: Iterable[models.Unit]
) -> list[models.UnitBeingLateCertificatesTodayAndWeekBefore | models.SingleUnitBeingLateCertificatesTodayAndWeekBefore]:
    account_name_to_units = utils.helpers.group_units_by_account_name(units)

    tasks = []
    for account_name, units in account_name_to_units.items():
        unit_ids = {unit.id for unit in units}
        cookies = await db.get_cookies(account_name)
        tasks.append(api.get_being_late_certificates_statistics(unit_ids, cookies))
    responses = await asyncio.gather(*tasks)

    result = []
    for response in responses:
        if isinstance(response, models.SingleUnitBeingLateCertificatesTodayAndWeekBefore):
            result.append(response)
        else:
            result += response
    return result
