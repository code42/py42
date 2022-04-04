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
    minutes = int(float(days) * 1440)
    return str(minutes)


def minutes_to_days(minutes):
    minutes = int(minutes)
    days = minutes / 1440
    if isinstance(days, float) and days.is_integer():
        return int(days)
    return days


def bytes_to_gb(bytes):
    if bytes == -1:  # special "unlimited" value
        return bytes
    gb = bytes / 1000**3
    if isinstance(gb, float) and gb.is_integer():
        return int(gb)
    return gb


def gb_to_bytes(gb):
    if gb == -1:  # special "unlimited" value
        return gb
    try:
        return gb * 1000**3
    except ValueError:
        raise AttributeError("value must be numeric.")
