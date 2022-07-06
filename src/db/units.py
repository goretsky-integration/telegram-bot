import models
from db.engine import database

__all__ = (
    'get_regions',
    'get_units_by_region',
    'get_units',
)


async def get_regions() -> list[str]:
    return await database.units.distinct('region')


async def get_units_by_region(region: str) -> list[models.Unit]:
    units = database.units.find({'region': region})
    return [models.Unit(id=unit['_id'], name=unit['name'], uuid=unit['uuid'],
                        account_name=unit['account_name'], region=unit['region'])
            async for unit in units]


async def get_units() -> list[models.Unit]:
    units = database.units.find({})
    return [models.Unit(id=unit['_id'], name=unit['name'], uuid=unit['uuid'],
                        account_name=unit['account_name'], region=unit['region'])
            async for unit in units]
