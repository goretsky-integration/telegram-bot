import pendulum

__all__ = (
    'humanize_percents',
    'humanize_seconds',
    'intgaps',
    'abbreviate_department_name',
)


def humanize_percents(percent: int | float) -> str:
    """Make percents more readable.

    Examples:
        >>> humanize_percents(54)
        '+54%'
        >>> humanize_percents(-4)
        '-4%'
        >>> humanize_percents(0)
        '0%'

    Args:
        percent: Any number.

    Returns:
        Readable percent.
    """
    percent_sign = '+' if percent > 0 else ''
    return f'{percent_sign}{percent}%'


def intgaps(number: int | float) -> str:
    """Make big numbers more readable.

    Examples:
        >>> intgaps(43466456)
        '43 466 456'
        >>> intgaps(5435.5)
        '5 435.5'

    Args:
        number: Any number.

    Returns:
        Readable big digit.
    """
    return f'{number:_}'.replace('_', ' ')


def humanize_seconds(seconds: int) -> str:
    """Humanize time in seconds.

    Examples:
        >>> humanize_seconds(60)
        '01:00'
        >>> humanize_seconds(0)
        '00:00'
        >>> humanize_seconds(3600)
        '01:00:00'
        >>> humanize_seconds(9000000)
        '+99:59:59'

    Args:
        seconds: Time in seconds.

    Returns:
        Humanized time in HH:MM:SS or MM:SS format.
        If there are over 100 hours (359999 seconds), returns "+99:59:59".
    """
    if seconds > 359999:
        return '+99:59:59'
    duration = pendulum.Duration(seconds=seconds)
    hours = duration.hours + duration.days * 24
    if not hours:
        return f'{duration.minutes:02}:{duration.remaining_seconds:02}'
    return f'{hours:02}:{duration.minutes:02}:{duration.remaining_seconds:02}'


def abbreviate_department_name(department_name: str) -> str:
    """Contract department name via abbreviations.

    Examples:
        >>> abbreviate_department_name('Москва 4-1')
        '4-1'
        >>> abbreviate_department_name('Вязьма-2')
        'ВЗМ-2'
        >>> abbreviate_department_name('Калуга-4')
        'КЛ-4'

    Args:
        department_name: Department name.

    Returns:
        Contracted department name or department name itself without changes
        if department name is not in special replacing map.
    """
    replacing_map = {
        'вязьма': 'ВЗМ',
        'калуга': 'КЛ',
        'смоленск': 'СМ',
        'обнинск': 'ОБН',
        'москва': '',
        'подольск': 'П',
    }
    for replaceable, replace_to in replacing_map.items():
        if replaceable in department_name.lower():
            return department_name.lower().replace(replaceable, replace_to).lstrip()
    return department_name

