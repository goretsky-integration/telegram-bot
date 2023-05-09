from datetime import datetime
from uuid import uuid4

import factory
from dodo_is_api.models import CourierOrder
from faker import Faker
from pytest_factoryboy import register

fake = Faker()


@register
class CourierOrderFactory(factory.Factory):
    class Meta:
        model = CourierOrder

    courier_staff_id = uuid4()
    delivery_time = fake.pyint(min_value=1, max_value=1000)
    delivery_transport_name = fake.word()
    handed_over_to_delivery_at = datetime.now()
    handed_over_to_delivery_at_local = datetime.now()
    heated_shelf_time = fake.pyint(min_value=1, max_value=1000)
    is_false_delivery = fake.pybool()
    is_problematic_delivery = fake.pybool()
    order_assembly_average_time = fake.pyint(min_value=1, max_value=1000)
    order_fulfilment_flag_at = datetime.now()
    order_id = uuid4()
    order_number = fake.word()
    predicted_delivery_time = fake.pyint(min_value=1, max_value=1000)
    problematic_delivery_reason = fake.word()
    trip_orders_count = fake.pyint(min_value=1, max_value=10)
    unit_uuid = uuid4()
    unit_name = fake.word()
    was_late_delivery_voucher_given = fake.pybool()
