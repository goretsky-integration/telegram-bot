from collections import defaultdict
from collections.abc import Iterable
from typing import TypeVar, Protocol
from uuid import UUID

from aiogram.types import User, Chat

from models import ChatToCreate
from models.api_responses import database as models
from models.mappers import RegionUnits


def group_units_by_region(
        *,
        units: Iterable[models.Unit],
        regions: Iterable[models.Region],
) -> list[RegionUnits]:
    region_id_to_units: defaultdict[int, list[models.Unit]] = defaultdict(list)
    for unit in units:
        region_id_to_units[unit.region_id].append(unit)
    return [
        RegionUnits(
            region=region,
            units=region_id_to_units[region.id],
        ) for region in regions
    ]


def map_user_to_create_dto(user: User) -> ChatToCreate:
    return ChatToCreate(
        id=user.id,
        type='PRIVATE',
        title=user.full_name,
        username=user.username,
    )


def map_chat_to_create_dto(chat: Chat) -> ChatToCreate:
    match chat.type:
        case 'group' | 'supergroup':
            chat_type = 'GROUP'
        case 'private':
            chat_type = 'PRIVATE'
        case _ as other_chat_type:
            raise ValueError(f'Invalid chat type "{other_chat_type}"')

    return ChatToCreate(
        id=chat.id,
        title=chat.full_name,
        username=chat.username,
        type=chat_type,
    )


class HasUnitUUID(Protocol):
    unit_uuid: UUID


ItemWithUnitUUIDT = TypeVar('ItemWithUnitUUIDT', bound=HasUnitUUID)


def group_by_unit_uuid(
        items: Iterable[ItemWithUnitUUIDT],
) -> dict[UUID, list[ItemWithUnitUUIDT]]:
    unit_uuid_to_items: defaultdict[UUID, list[ItemWithUnitUUIDT]] = (
        defaultdict(list)
    )
    for item in items:
        unit_uuid_to_items[item.unit_uuid].append(item)
    return dict(unit_uuid_to_items)
