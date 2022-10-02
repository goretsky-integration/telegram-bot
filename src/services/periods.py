import pendulum

__all__ = (
    'get_last_7_days_period',
    'get_last_14_days_period',
    'get_last_30_days_period',
)


MOSCOW_TZ = pendulum.timezone('Europe/Moscow')


def get_moscow_now() -> pendulum.DateTime:
    return pendulum.now(MOSCOW_TZ)


def get_period_from(days: int) -> pendulum.Period:
    now = get_moscow_now()
    return pendulum.Period(start=now.subtract(days=days), end=now)


def get_last_7_days_period() -> pendulum.Period:
    return get_period_from(days=7)


def get_last_14_days_period() -> pendulum.Period:
    return get_period_from(days=14)


def get_last_30_days_period() -> pendulum.Period:
    return get_period_from(days=30)
