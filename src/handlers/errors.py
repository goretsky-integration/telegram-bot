from aiogram.types import Update
from aiogram.utils.exceptions import MessageNotModified

from bot import dp
from utils import exceptions


@dp.errors_handler(exception=exceptions.NoneUnitIdsSetUpError)
async def on_none_unit_ids_set_up_error(update: Update, exception: MessageNotModified):
    text = ('Кажется вы не добавили ни одну точку продаж для отображения 😕\n'
            'Чтобы это сделать, нажмите на кнопку ⚙️ Настройки или введите команду /settings.\n'
            'Далее нажмите на кнопку Отчёты по статистике и отметьте точки продаж.')
    if update.callback_query is not None:
        await update.callback_query.message.answer(text)
        await update.callback_query.answer()
    elif update.message is not None:
        await update.message.answer(text)
    return True


@dp.errors_handler(exception=MessageNotModified)
async def on_message_not_modified_error(update: Update, exception: MessageNotModified):
    if update.callback_query is not None:
        await update.callback_query.answer('Обновлено ✅')
    elif update.message is not None:
        await update.message.answer('Обновлено ✅')
    return True


@dp.errors_handler(exception=exceptions.DodoAPIError)
async def on_dodo_api_error(update: Update, exception: exceptions.DodoAPIError):
    if update.callback_query is not None:
        await update.callback_query.answer('Произошла ошибка', show_alert=True)
    elif update.message is not None:
        await update.message.answer('Произошла ошибка')
    return True
