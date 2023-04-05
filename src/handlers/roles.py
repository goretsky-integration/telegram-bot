import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, Command
from aiogram.types import (
    Message, CallbackQuery, Update, InlineKeyboardMarkup,
    InlineKeyboardButton
)

from core import exceptions
from services.database_api import DatabaseAPIService
from services.http_client_factory import HTTPClientFactory
from services.mappers import group_units_by_region
from shortcuts import answer_views, get_message
from utils.states import SetUserRoleStates
from views import RoleMenuView


async def on_user_has_no_role_error(
        update: Update,
        exception: exceptions.UserHasNoRoleError,
):
    message = get_message(update)
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    'Установить роль',
                    callback_data='set_role',
                )
            ]
        ]
    )
    await message.answer(
        'Вы не можете использовать бота, так как у вас не установлена роль 😕',
        reply_markup=markup,
    )
    return True


async def on_role_not_found_error(
        update: Update,
        exception: exceptions.RoleNotFoundError,
):
    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                'Попробовать ещё раз',
                callback_data='set_role',
            )],
        ]
    )
    await update.message.reply(
        'Роль не найдена. Кажется, введенный код неверный. 😔',
        reply_markup=markup,
    )
    dispatcher = Dispatcher.get_current(no_error=False)
    await dispatcher.storage.finish(
        chat=update.message.chat.id,
        user=update.message.from_user.id
    )
    return True


async def set_user_role(
        message: Message,
        state: FSMContext,
        database_api_http_client_factory: HTTPClientFactory,
):
    access_code = message.text
    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)
        await database_api_service.set_user_role(
            chat_id=message.from_user.id,
            access_code=access_code,
        )

    markup = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton('Посмотреть мои доступы',
                                  callback_data='my_role')],
        ],
    )
    await message.answer('Ваша роль изменена 🤩', reply_markup=markup)
    await message.delete()
    await state.finish()


async def require_role_access_code(
        callback_query: CallbackQuery,
):
    await callback_query.message.answer('Введите ваш код')
    await SetUserRoleStates.access_code.set()
    await callback_query.answer()


async def show_role_menu(
        query: Message | CallbackQuery,
        database_api_http_client_factory: HTTPClientFactory,
):
    async with database_api_http_client_factory() as http_client:
        database_api_service = DatabaseAPIService(http_client)
        try:
            async with asyncio.TaskGroup() as task_group:
                units = task_group.create_task(
                    database_api_service.get_role_units(
                        chat_id=query.from_user.id,
                    ),
                )
                report_types = task_group.create_task(
                    database_api_service.get_role_report_types(
                        chat_id=query.from_user.id,
                    ),
                )
                regions = task_group.create_task(
                    database_api_service.get_role_regions(
                        chat_id=query.from_user.id,
                    ),
                )
        except ExceptionGroup as eg:
            for exc in eg.exceptions:
                raise exc

    units, report_types, regions = [
        task.result() for task in (units, report_types, regions)
    ]
    region_units = group_units_by_region(units=units, regions=regions)
    view = RoleMenuView(region_units=region_units, report_types=report_types)
    message = query.message if isinstance(query, CallbackQuery) else query
    await answer_views(message, view)


def register_message_handlers(dispatcher: Dispatcher):
    dispatcher.register_errors_handler(
        on_user_has_no_role_error,
        exception=exceptions.UserHasNoRoleError,
    )
    dispatcher.register_errors_handler(
        on_role_not_found_error,
        exception=exceptions.RoleNotFoundError,
    )
    dispatcher.register_message_handler(
        show_role_menu,
        Text('🙎‍♂️ Моя роль') | Command('my_role'),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        show_role_menu,
        Text('my_role'),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        require_role_access_code,
        Text('set_role'),
        state='*',
    )
    dispatcher.register_message_handler(
        set_user_role,
        state=SetUserRoleStates.access_code,
    )
