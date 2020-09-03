from py42._compat import str


def bool_to_str(value):
    if isinstance(value, bool) or value in ("true", "false"):
        return str(value).lower()
    else:
        raise ValueError("Value must be True or False")


def str_to_bool(value):
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    else:
        return value


def to_list(value):
    if isinstance(value, (list, tuple)):
        return value
    else:
        return [value]


def days_to_minutes(days):
    return str(int(float(days) * 1440))


def minutes_to_days(minutes):
    minutes = int(minutes)
    return int(minutes / 1440)


def no_conversion(x):
    return x
