from typing import Iterable

from pymongo.results import UpdateResult

from db.engine import database

__all__ = (
    'insert_unit_by_report_type_and_chat_id',
    'delete_unit_by_report_type_and_chat_id',
    'get_unit_ids_by_report_type_and_chat_id',
)


async def insert_unit_by_report_type_and_chat_id(
        report_type: str, chat_id: int, unit_ids: Iterable[int],
) -> str | None:
    report: UpdateResult = await database.reports.update_one(
        {'$and': [{'report_type': report_type}, {'chat_id': chat_id}]},
        {'$addToSet': {'unit_ids': {'$each': tuple(unit_ids)}}},
        upsert=True,
    )
    return report.upserted_id


async def delete_unit_by_report_type_and_chat_id(report_type: str, chat_id: int, unit_ids: Iterable[int]):
    await database.reports.update_one(
        {'$and': [{'report_type': report_type}, {'chat_id': chat_id}]},
        {'$pull': {'unit_ids': {'$in': tuple(unit_ids)}}},
    )


async def get_unit_ids_by_report_type_and_chat_id(report_type: str, chat_id: int) -> list[int]:
    result = await database.reports.find_one({'$and': [{'report_type': report_type}, {'chat_id': chat_id}]})
    if result is None:
        return []
    return result['unit_ids']
