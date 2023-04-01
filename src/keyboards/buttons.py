from aiogram.types import InlineKeyboardButton, KeyboardButton

import models.api_responses.database as models
from utils import callback_data

__all__ = (
    'UpdateStatisticsButton',
    'SettingsButton',
    'StatisticsReportsButton',
    'ShowStatisticsButton',
    'ChooseRegionButton',
    'ReportSettingsButton',
    'SwitchUnitStatusButton',
    'DisableAllUnitsByRegionButton',
    'EnableAllUnitsByRegionButton',
)


class StatisticsReportsButton(KeyboardButton):

    def __init__(self):
        super().__init__(text='📊 Отчёты/Статистика')


class SettingsButton(KeyboardButton):

    def __init__(self):
        super().__init__(text='⚙️ Настройки')


class UpdateStatisticsButton(InlineKeyboardButton):

    def __init__(self, report_name: str):
        super().__init__(
            text='🔄 Обновить',
            callback_data=callback_data.show_statistics.new(name=report_name),
        )


class ShowStatisticsButton(InlineKeyboardButton):

    def __init__(self, statistics: models.ReportType):
        super().__init__(
            text=statistics.verbose_name,
            callback_data=callback_data.show_statistics.new(
                report_type_name=statistics.name)
        )


class ReportSettingsButton(InlineKeyboardButton):

    def __init__(self, report_type: models.ReportType):
        super().__init__(
            text=report_type.verbose_name,
            callback_data=callback_data.ReportSettingsCallbackData().new(
                report_type_id=report_type.id,
            )
        )


class ChooseRegionButton(InlineKeyboardButton):

    def __init__(self, report_type_id: int, region: models.Region):
        callback_data_factory = callback_data.UnitsByRegionCallbackData()
        super().__init__(
            text=region.name,
            callback_data=callback_data_factory.new(
                region_id=region.id,
                report_type_id=report_type_id,
            ),
        )


class SwitchUnitStatusButton(InlineKeyboardButton):

    def __init__(
            self,
            report_type_id: int,
            region_id: int,
            unit_id: int,
            unit_name: str,
            is_unit_enabled: bool,
    ):
        super().__init__(
            text=f'{"🟢" if is_unit_enabled else "🔴"} {unit_name}',
            callback_data=callback_data.SwitchUnitStatusCallbackData().new(
                report_type_id=report_type_id,
                unit_id=unit_id,
                region_id=region_id,
                is_unit_enabled=int(is_unit_enabled),
            )
        )


class EnableAllUnitsByRegionButton(InlineKeyboardButton):

    def __init__(self, report_type_id: int, region_id: int):
        super().__init__(
            text='Включить все',
            callback_data=callback_data.SwitchAllUnitStatusesCallbackData().new(
                report_type_id=report_type_id,
                region_id=region_id,
                action='enable'
            ),
        )


class DisableAllUnitsByRegionButton(InlineKeyboardButton):

    def __init__(self, report_type_id: int, region_id: int):
        super().__init__(
            text='Отключить все',
            callback_data=callback_data.SwitchAllUnitStatusesCallbackData().new(
                report_type_id=report_type_id,
                region_id=region_id,
                action='disable'
            ),
        )
