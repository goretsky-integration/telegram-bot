import pendulum

__all__ = (
    'get_period_from',
)

MOSCOW_TZ = pendulum.timezone('Europe/Moscow')


def get_moscow_now() -> pendulum.DateTime:
    return pendulum.now(MOSCOW_TZ)


def get_period_from(days: int) -> pendulum.Period:
    now = get_moscow_now()
    return pendulum.Period(start=now.subtract(days=days), end=now)
