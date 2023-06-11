from collections.abc import Iterable
from typing import TypeAlias
from uuid import UUID

from dodo_is_api import models as dodo_is_api_models

from services.mappers import group_by_unit_uuid
from models.report_views import UnitLateDeliveryVouchersStatisticsViewDTO

LateDeliveryVouchers: TypeAlias = (
    Iterable[dodo_is_api_models.LateDeliveryVoucher]
)


def calculate_late_delivery_vouchers_count_for_today_and_week_before(
        vouchers_for_today: LateDeliveryVouchers,
        vouchers_for_week_before: LateDeliveryVouchers,
        unit_uuid_to_name: dict[UUID, str],
) -> list[UnitLateDeliveryVouchersStatisticsViewDTO]:
    vouchers_for_today_grouped_by_unit_uuid = (
        group_by_unit_uuid(vouchers_for_today)
    )
    vouchers_for_week_before_grouped_by_unit_uuid = (
        group_by_unit_uuid(vouchers_for_week_before)
    )

    units_late_delivery_vouchers_statistics: (
        list[UnitLateDeliveryVouchersStatisticsViewDTO]
    ) = []
    for unit_uuid, unit_name in unit_uuid_to_name.items():
        unit_vouchers_for_today = (
            vouchers_for_today_grouped_by_unit_uuid.get(unit_uuid, [])
        )
        unit_vouchers_for_week_before = (
            vouchers_for_week_before_grouped_by_unit_uuid.get(unit_uuid, [])
        )
        unit_vouchers_for_today_count = len(unit_vouchers_for_today)
        unit_vouchers_for_week_before_count = len(unit_vouchers_for_week_before)

        units_late_delivery_vouchers_statistics.append(
            UnitLateDeliveryVouchersStatisticsViewDTO(
                unit_name=unit_name,
                certificates_count_today=unit_vouchers_for_today_count,
                certificates_count_week_before=(
                    unit_vouchers_for_week_before_count
                ),
            )
        )

    return units_late_delivery_vouchers_statistics
