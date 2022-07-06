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

    def __init__(self, statistics: models.database.StatisticsReportType):
        super().__init__(
            text=statistics.value,
            callback_data=callback_data.show_statistics.new(name=statistics.name)
        )


class ReportSettingsButton(InlineKeyboardButton):

    def __init__(self, report: models.database.ReportType):
        super().__init__(
            text=report.value,
            callback_data=callback_data.report_settings.new(name=report.name)
        )


class ChooseRegionButton(InlineKeyboardButton):

    def __init__(self, report_type: str, region: str):
        super().__init__(
            text=region,
            callback_data=callback_data.units_by_region.new(
                region=region,
                report_type=report_type,
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
