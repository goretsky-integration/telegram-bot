from aiogram.utils.callback_data import CallbackData

import models

__all__ = (
    'show_statistics',
    'ReportSettingsCallbackData',
    'UnitsByRegionCallbackData',
    'SwitchUnitStatusCallbackData',
    'SwitchAllUnitStatusesCallbackData',
)


class ReportSettingsCallbackData(CallbackData):

    def __init__(self):
        super().__init__(
            '2',
            'report_type_id',
        )

    def parse(self, callback_data: str) -> models.ReportTypeCallbackData:
        callback_data = super().parse(callback_data)
        return {'report_type_id': int(callback_data['report_type_id'])}


class UnitsByRegionCallbackData(CallbackData):

    def __init__(self):
        super().__init__('3', 'region_id', 'report_type_id')

    def parse(self, callback_data: str) -> models.UnitsByRegionCallbackData:
        callback_data = super().parse(callback_data)
        return {
            'report_type_id': int(callback_data['report_type_id']),
            'region_id': int(callback_data['region_id']),
        }


class SwitchUnitStatusCallbackData(CallbackData):

    def __init__(self):
        super().__init__('4', 'unit_id', 'report_type_id',
                         'is_unit_enabled', 'region_id')

    def parse(self, callback_data: str) -> models.SwitchUnitStatusCallbackData:
        callback_data = super().parse(callback_data)
        return {
            'unit_id': int(callback_data['unit_id']),
            'report_type_id': int(callback_data['report_type_id']),
            'is_unit_enabled': callback_data['is_unit_enabled'] == '1',
            'region_id': int(callback_data['region_id']),
        }


class SwitchAllUnitStatusesCallbackData(CallbackData):

    def __init__(self):
        super().__init__('5', 'report_type_id', 'action', 'region_id')

    def parse(
            self,
            callback_data: str,
    ) -> models.AllUnitIdsByRegionCallbackData:
        callback_data = super().parse(callback_data)
        return {
            'action': callback_data['action'],
            'region_id': int(callback_data['region_id']),
            'report_type_id': int(callback_data['report_type_id']),
        }


show_statistics = CallbackData('1', 'report_type_name')
