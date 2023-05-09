from dataclasses import dataclass
from datetime import datetime
from typing import Callable, TypeAlias
from zoneinfo import ZoneInfo

__all__ = ('Period',)

DatetimeFactory: TypeAlias = Callable[[], datetime]


@dataclass(frozen=True, slots=True)
class Period:
    start: datetime
    end: datetime

    @classmethod
    def today_to_this_time(cls, *, timezone: ZoneInfo | None = None):
        if timezone is None:
            timezone = ZoneInfo('UTC')
        now = datetime.now(timezone)
        return cls(
            start=datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                tzinfo=timezone,
            ),
            end=datetime(
                year=now.year,
                month=now.month,
                day=now.day,
                hour=now.hour,
                minute=now.minute,
                second=now.second,
                microsecond=now.microsecond,
                tzinfo=timezone,
            )
        )
