from aiogram.utils.callback_data import CallbackData

__all__ = (
    'show_statistics',
    'report_settings',
    'units_by_region',
    'switch_unit_status',
)


show_statistics = CallbackData('show_statistics', 'name')
report_settings = CallbackData('report_settings', 'name')
units_by_region = CallbackData('units_by_region', 'region', 'report_type')
switch_unit_status = CallbackData('switch_unit_status', 'unit_id', 'report_type', 'is_unit_enabled', 'region')
