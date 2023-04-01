from collections.abc import Iterable

from aiogram.types import InlineKeyboardMarkup

import models.api_responses.database as models
from keyboards import buttons

__all__ = (
    'UpdateStatisticsReportMarkup',
    'StatisticsReportsMarkup',
    'RegionsMarkup',
    'SettingsMarkup',
    'UnitsMarkup',
)


class UpdateStatisticsReportMarkup(InlineKeyboardMarkup):

    def __init__(self, report_name: str):
        super().__init__()
        self.add(
            buttons.UpdateStatisticsButton(report_name),
        )


class StatisticsReportsMarkup(InlineKeyboardMarkup):

    def __init__(self, statistics_report_types: Iterable[models.ReportType]):
        super().__init__(row_width=1)
        self.add(
            *(buttons.ShowStatisticsButton(statistics_type) for statistics_type
              in statistics_report_types))


class SettingsMarkup(InlineKeyboardMarkup):

    def __init__(self, report_types: Iterable[models.ReportType]):
        super().__init__(row_width=1)
        self.add(
            *(buttons.ReportSettingsButton(report) for report in report_types))


class RegionsMarkup(InlineKeyboardMarkup):

    def __init__(self, report_type_id: int, regions: Iterable[models.Region]):
        super().__init__(row_width=1)
        self.add(
            *(buttons.ChooseRegionButton(report_type_id, region) for region in
              regions))


class UnitsMarkup(InlineKeyboardMarkup):

    def __init__(self, report_type_id: int, region_id: int,
                 enabled_unit_ids: Iterable[int],
                 all_units: Iterable[models.Unit]):
        super().__init__(row_width=2)
        self.__report_type_id = report_type_id
        self.__region_id = region_id
        self.__all_units = all_units
        self.__enabled_unit_ids = set(enabled_unit_ids)

        self.__add_unit_operations()
        self.__add_batch_operations()

    @property
    def __all_unit_ids(self) -> set[int]:
        return {unit.id for unit in self.__all_units}

    @property
    def __disabled_unit_ids(self) -> set[int]:
        return self.__all_unit_ids - self.__enabled_unit_ids

    def __add_unit_operations(self) -> None:
        for unit in self.__all_units:
            is_unit_enabled = unit.id in self.__enabled_unit_ids
            button = buttons.SwitchUnitStatusButton(
                report_type_id=self.__report_type_id,
                region_id=self.__region_id,
                unit_id=unit.id,
                unit_name=unit.name,
                is_unit_enabled=is_unit_enabled,
            )
            self.insert(button)

    def __add_batch_operations(self) -> None:
        row = []
        if any(self.__disabled_unit_ids):
            row.append(buttons.EnableAllUnitsByRegionButton(
                report_type_id=self.__report_type_id,
                region_id=self.__region_id,
            ))
        if any(self.__enabled_unit_ids):
            row.append(buttons.DisableAllUnitsByRegionButton(
                report_type_id=self.__report_type_id,
                region_id=self.__region_id,
            ))
        self.row(*row)

