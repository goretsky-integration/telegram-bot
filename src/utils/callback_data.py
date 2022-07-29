from aiogram.utils.callback_data import CallbackData

__all__ = (
    'show_statistics',
    'report_settings',
    'units_by_region',
    'switch_unit_status',
    'switch_all_unit_statuses',
)


show_statistics = CallbackData('1', 'report_type_name')
report_settings = CallbackData('2', 'report_type_name')
units_by_region = CallbackData('3', 'region', 'report_type_name')
switch_unit_status = CallbackData('4', 'unit_id', 'report_type', 'is_unit_enabled', 'region')
switch_all_unit_statuses = CallbackData('5', 'report_type', 'action', 'region')
