import pytest

from fixtures.courier_orders import CourierOrderFactory
from services.domain.orders import calculate_trips_with_one_order_percentage


@pytest.mark.parametrize(
    'orders, percentage',
    [
        (
                CourierOrderFactory.create_batch(size=5, trip_orders_count=1)
                + CourierOrderFactory.create_batch(size=4, trip_orders_count=2)
                + CourierOrderFactory.create_batch(
                    size=12, trip_orders_count=3),
                45,
        ),
        (
                CourierOrderFactory.create_batch(size=28, trip_orders_count=1)
                + CourierOrderFactory.create_batch(size=52, trip_orders_count=2)
                + CourierOrderFactory.create_batch(size=33, trip_orders_count=3)
                + CourierOrderFactory.create_batch(
                    size=24, trip_orders_count=4),
                39,
        ),
    ]
)
def test_calculate_trips_with_one_order_percentage(orders, percentage):
    assert calculate_trips_with_one_order_percentage(orders) == percentage


def test_no_courier_orders_provided():
    assert calculate_trips_with_one_order_percentage([]) == 0
