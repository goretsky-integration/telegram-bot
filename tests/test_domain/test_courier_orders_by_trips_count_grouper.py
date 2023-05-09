from services.domain.orders import group_courier_orders_by_trips_count


def test_group_courier_orders_by_trips_count(courier_order_factory):
    orders = [
        courier_order_factory(trip_orders_count=1),
        courier_order_factory(trip_orders_count=2),
        courier_order_factory(trip_orders_count=1),
        courier_order_factory(trip_orders_count=3),
        courier_order_factory(trip_orders_count=2),
    ]

    grouped_orders = group_courier_orders_by_trips_count(orders)

    # check that the orders are grouped correctly
    assert len(grouped_orders) == 3
    assert len(grouped_orders[1]) == 2
    assert len(grouped_orders[2]) == 2
    assert len(grouped_orders[3]) == 1

    # check that each order is in the correct group
    for order in orders:
        assert order in grouped_orders[order.trip_orders_count]
