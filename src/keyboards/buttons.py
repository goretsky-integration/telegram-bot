from aiogram.types import InlineKeyboardButton, KeyboardButton

import models
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

    def __init__(self, statistics: models.StatisticsReportType):
        super().__init__(
            text=statistics.verbose_name,
            callback_data=callback_data.show_statistics.new(report_type_name=statistics.name)
        )


class ReportSettingsButton(InlineKeyboardButton):

    def __init__(self, report_type: models.ReportType):
        super().__init__(
            text=report_type.verbose_name,
            callback_data=callback_data.report_settings.new(report_type_name=report_type.name)
        )


class ChooseRegionButton(InlineKeyboardButton):

    def __init__(self, report_type_name: str, region: str):
        super().__init__(
            text=region,
            callback_data=callback_data.units_by_region.new(
                region=region,
                report_type_name=report_type_name,
            ),
        )


class SwitchUnitStatusButton(InlineKeyboardButton):

    def __init__(self, report_type: str, region: str, unit_id: int, unit_name: str, is_unit_enabled: bool):
        super().__init__(
            text=f'{"🟢" if is_unit_enabled else "🔴"} {unit_name}',
            callback_data=callback_data.switch_unit_status.new(
                report_type=report_type,
                unit_id=unit_id,
                region=region,
                is_unit_enabled=int(is_unit_enabled),
            )
        )


class EnableAllUnitsByRegionButton(InlineKeyboardButton):

    def __init__(self, report_type: str, region: str):
        super().__init__(
            text='Включить все',
            callback_data=callback_data.switch_all_unit_statuses.new(
                report_type=report_type,
                region=region,
                action='enable'
            ),
        )


class DisableAllUnitsByRegionButton(InlineKeyboardButton):

    def __init__(self, report_type: str, region: str):
        super().__init__(
            text='Отключить все',
            callback_data=callback_data.switch_all_unit_statuses.new(
                report_type=report_type,
                region=region,
                action='disable',
            ),
        )
