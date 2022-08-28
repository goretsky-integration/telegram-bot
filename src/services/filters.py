from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery

from services.dependencies import get_db_client
from utils import logger, convert_models, constants

__all__ = (
    'UnitIdsRequiredFilter',
)


class UnitIdsRequiredFilter(BoundFilter):

    async def check(self, query: Message | CallbackQuery) -> bool | dict:
        logger.debug(f'Statistics report unit ids filter')
        message = query.message if isinstance(query, CallbackQuery) else query
        async with get_db_client() as db:
            enabled_reports = await db.get_reports(report_type=constants.ReportType.STATISTICS.name,
                                                   chat_id=message.chat.id)
            enabled_unit_ids = [unit_id for report in enabled_reports for unit_id in report.unit_ids]
            logger.debug(enabled_unit_ids)
            if not enabled_unit_ids:
                return False
            units = await db.get_units()
            enabled_units = [unit for unit in units if unit.id in enabled_unit_ids]
            return {'units': convert_models.UnitsConverter(enabled_units)}
