from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message, CallbackQuery

import db
import models
from utils import logger

__all__ = (
    'EnabledUnitIdsFilter',
)


class EnabledUnitIdsFilter(BoundFilter):

    async def check(self, query: Message | CallbackQuery) -> bool | dict:
        logger.debug(f'Statistics report unit ids filter')
        message = query.message if isinstance(query, CallbackQuery) else query
        enabled_unit_ids = await db.get_unit_ids_by_report_type_and_chat_id(models.ReportType.STATISTICS.name,
                                                                            message.chat.id)
        if enabled_unit_ids:
            return {'enabled_unit_ids': enabled_unit_ids}
