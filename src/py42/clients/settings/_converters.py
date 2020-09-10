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
        raise ValueError("str_to_bool expects either 'true' or 'false'.")


def to_list(value):
    if isinstance(value, (list, tuple)):
        return value
    else:
        return [value]


def to_comma_separated(value):
    if isinstance(value, (list, tuple)):
        return ",".join(value)
    else:
        return value


def comma_separated_to_list(value):
    return value.split(",")


def days_to_minutes(days):
    return str(int(float(days) * 1440))


def minutes_to_days(minutes):
    minutes = int(minutes)
    return int(minutes / 1440)


def bytes_to_gb(bytes):
    gb = bytes / 1000 ** 3
    if gb.is_integer():
        return int(gb)
    return gb


def gb_to_bytes(gb):
    try:
        return gb * 1000 ** 3
    except ValueError:
        raise AttributeError("value must be numeric.")


def no_conversion(x):
    return x
