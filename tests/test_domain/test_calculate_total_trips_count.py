import pytest

from services.domain.orders import calculate_total_trips_count


@pytest.fixture
def courier_orders_grouped_by_trips_count(courier_order_factory):
    return {
        0: [],
        1: courier_order_factory.create_batch(size=7, trip_orders_count=1),
        2: courier_order_factory.create_batch(size=6, trip_orders_count=2),
        3: courier_order_factory.create_batch(size=9, trip_orders_count=3)
    }


def test_calculate_total_trips_count(courier_orders_grouped_by_trips_count):
    actual = calculate_total_trips_count(courier_orders_grouped_by_trips_count)
    assert actual == 13


def test_calculate_total_trips_count_no_orders_provided():
    assert calculate_total_trips_count({}) == 0
