import string

from rumps import (
    alert,
)

from src.exceptions import (
    ValidationError,
)


def wait_for_result(window, validators=None, timeout=0.1):
    """Wait for a valid result to be received by the ``window`` specified.

    Using a ``rumps`` window is expected in this case, where we use the common
    while loop pattern with a default timeout to loop and check the current windows
    result.

    Any validators passed in will be ran sequentially on the value taken from
    the window instance.
    """
    while True:
        result = window.run()

        if result.clicked == 0:
            return

        text = result.text

        if validators:
            try:
                for validator in validators:
                    validator(text)
            except ValidationError as err:
                alert(
                    title=err.title,
                    message=err.message,
                )
                window.default_text = text
                continue

        return text


def strfdelta(delta, fmt="{H:02}h {M:02}m {S:02}s", typ="timedelta"):
    """Convert a datetime.timedelta object or a regular number to a custom-
    formatted string, just like the stftime() method does for datetime.datetime
    objects.

    The fmt argument allows custom formatting to be specified.  Fields can
    include seconds, minutes, hours, days, and weeks.  Each field is optional.

    Some examples:
        "{H:02}h {M:02}m {S:02}s          --> "08h 04m 02s" (default)
        "{D:02}d {H:02}h {M:02}m {S:02}s" --> "05d 08h 04m 02s"
        "{W}w {D}d {H}:{M:02}:{S:02}"     --> "4w 5d 8:04:02"
        "{D:2}d {H:2}:{M:02}:{S:02}"      --> " 5d  8:04:02"
        "{H}h {S}s"                       --> "72h 800s"

    The typ argument allows delta to be a regular number instead of the
    default, which is a datetime.timedelta object. Valid typ strings:
        "s", "seconds",
        "m", "minutes",
        "h", "hours",
        "d", "days",
        "w", "weeks"
    """
    remainder = None

    if typ == "timedelta":
        remainder = int(delta.total_seconds())
    elif typ in ["s", "seconds"]:
        remainder = int(delta)
    elif typ in ["m", "minutes"]:
        remainder = int(delta) * 60
    elif typ in ["h", "hours"]:
        remainder = int(delta) * 3600
    elif typ in ["d", "days"]:
        remainder = int(delta) * 86400
    elif typ in ["w", "weeks"]:
        remainder = int(delta) * 604800

    f = string.Formatter()

    desired_fields = [
        field_tuple[1] for field_tuple in f.parse(fmt)
    ]
    possible_fields = (
        "W",
        "D",
        "H",
        "M",
        "S",
    )
    constants = {
        "W": 604800,
        "D": 86400,
        "H": 3600,
        "M": 60,
        "S": 1,
    }
    values = {}
    for field in possible_fields:
        if field in desired_fields and field in constants:
            values[field], remainder = divmod(remainder, constants[field])
    return f.format(fmt, **values)
