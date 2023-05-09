from collections import defaultdict
from collections.abc import Iterable, Mapping
from typing import TypeAlias

from dodo_is_api.models import CourierOrder

CourierOrdersGroupedByTripsCount: TypeAlias = Mapping[int, list[CourierOrder]]


def group_courier_orders_by_trips_count(
        courier_orders: Iterable[CourierOrder],
) -> CourierOrdersGroupedByTripsCount:
    """Group courier orders by the count of orders in one trip.

    Args:
        courier_orders: Collection of courier orders.

    Returns:
        Mapping, where key is orders per trip
         and value is a collection of courier orders.
    """
    orders_grouped_by_trips_count: CourierOrdersGroupedByTripsCount = (
        defaultdict(list)
    )

    for order in courier_orders:
        courier_orders = orders_grouped_by_trips_count[order.trip_orders_count]
        courier_orders.append(order)

    return orders_grouped_by_trips_count


def calculate_total_trips_count(
        orders_grouped_by_trips_count: CourierOrdersGroupedByTripsCount
) -> int:
    """
    To calculate the number of trips made by a courier,
    we divide the total number of orders by the number of orders per trip, N.

    For example,
    if each trip has 2 orders and there were a total of 14 orders,
    then there were 7 trips.

    Args:
        orders_grouped_by_trips_count: Mapping, where key is orders per trip
            and value is a collection of courier orders.

    Returns:
        Total count of trips.
    """
    return sum(
        len(orders) // trip_orders_count
        for trip_orders_count, orders in orders_grouped_by_trips_count.items()
        if trip_orders_count != 0
    )


def calculate_trips_with_one_order_percentage(
        courier_orders: Iterable[CourierOrder],
) -> int:
    """Calculate the percentage of courier trips that had only one order.

    Args:
        courier_orders: Collection of courier orders.

    Returns:
        Percentage of courier trips.
    """
    if not courier_orders:
        return 0

    courier_orders_grouped_by_trips_count = group_courier_orders_by_trips_count(
        courier_orders=courier_orders,
    )
    total_trips_count = calculate_total_trips_count(
        orders_grouped_by_trips_count=courier_orders_grouped_by_trips_count
    )
    trips_with_one_order = courier_orders_grouped_by_trips_count.get(1, [])
    trips_with_one_order_count = len(trips_with_one_order)
    return round(trips_with_one_order_count / total_trips_count * 100)
