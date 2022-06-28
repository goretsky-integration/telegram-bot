import itertools

import models
from db.engine import database

__all__ = (
    'get_regions',
    'get_units_by_region_id',
    'get_units',
)


async def get_regions() -> list[models.Region]:
    regions = database.units.find({}, {'region': 1})
    return [models.Region(id=region['_id'], name=region['region']) async for region in regions]


async def get_units_by_region_id(region_id: int) -> list[models.Unit]:
    result = await database.units.find_one({'_id': region_id}, {'_id': 0, 'region': 0})
    return [models.Unit(id=unit['_id'], name=unit['name'], uuid=unit['uuid'])
            for unit in result['units']]


async def get_units() -> list[models.Unit]:
    results = database.units.find({}, {'units': 1, '_id': 0})
    units_results = itertools.chain.from_iterable([result['units'] async for result in results])
    return [models.Unit(id=unit['_id'], name=unit['name'], uuid=unit['uuid'])
            for unit in units_results]
