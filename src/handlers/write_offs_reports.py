import tempfile

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery
from dodolib import DatabaseClient

from bot import dp
from responses import WriteOffsReportPeriodResponse
from services import periods, write_offs_api
from utils.callback_data import last_n_days_period


@dp.callback_query_handler(
    last_n_days_period.filter(),
    state='*',
)
async def on_prepopulated_write_offs_periods(callback_query: CallbackQuery,
                                             callback_data: dict,
                                             db: DatabaseClient):
    days_before_count = int(callback_data['days_before_count'])
    period = periods.get_period_from(days_before_count)
    write_offs_from_api = write_offs_api.get_write_offs_by_period(period)
    grouped_write_offs = write_offs_api.group_write_offs_by_unit(write_offs_from_api)

    units = await db.get_units()
    unit_ids_to_names = {unit.id: unit.name for unit in units}

    with tempfile.NamedTemporaryFile(prefix='Отчёт по списаниям ингредиентов ', suffix='.xlsx') as temp_file:
        write_offs_api.generate_write_offs_excel_report(temp_file.name, unit_ids_to_names, grouped_write_offs)
        with open(temp_file.name, 'rb') as file:
            await callback_query.message.answer_document(file)


@dp.message_handler(Command('write_offs_report'), state='*')
async def on_reports_button(message: Message):
    return await message.answer(**WriteOffsReportPeriodResponse().as_dict())
