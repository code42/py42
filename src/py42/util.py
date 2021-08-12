import json
from datetime import datetime

MICROSECOND_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DATE_STR_FORMAT = "%Y-%m-%d %H:%M:%S"


def format_json(json_string):
    """Converts a minified JSON str to a prettified JSON str.

    Args:
        json_string (str): A str representing minified JSON.

    Returns:
        (str): A str representing prettified JSON.
    """
    parsed = json.loads(json_string)
    return json.dumps(parsed, indent=4)


def print_response(response, label=None):
    """Prints a :class:`py42.response.Py42Response` as prettified JSON. If unable to load, it
    prints the given response.

    Args:
        response (:class:`py42.response.Py42Response`): The response to print.
        label (str, optional): A label at the beginning of the printed text. Defaults to None.
    """
    if label:
        print(label, end=" ")
    try:
        print(format_json(response.text))
    except ValueError:
        print(response)


def convert_timestamp_to_str(timestamp):
    """Converts the given POSIX timestamp to a date str. The format matches strftime
    directives %Y-%m-%dT%H:%M:%S.%f.

    Args:
        timestamp (float or int): A POSIX timestamp.

    Returns:
        (str): A str representing the given timestamp. Example output looks like
        '2020-03-25T15:29:04.465Z'.
    """
    date = datetime.utcfromtimestamp(timestamp)
    return convert_datetime_to_timestamp_str(date)


def convert_datetime_to_timestamp_str(date):
    """Converts the given datetime to a formatted date str. The format matches strftime
    directives %Y-%m-%dT%H:%M:%S.%f.

    Args:
        date (datetime): The datetime object to convert.

    Returns:
        (str): A str representing the given date. Example output looks like
        '2020-03-25T15:29:04.465Z'.
    """
    prefix = date.strftime(MICROSECOND_FORMAT)[:-4]
    return f"{prefix}Z"


def convert_datetime_to_epoch(date):
    return date.timestamp()


def format_dict(dict_, label=None):
    indented_dict = json.dumps(dict_, indent=4)
    if label:
        return f"{label} {indented_dict}"
    return indented_dict


def get_attribute_values_from_class(cls):
    """Returns attribute values for the given class.

    Args:
        cls (class): The class to obtain attributes from.

    Returns:
        (list): A list containing the attribute values of the given class.
    """
    return [
        cls().__getattribute__(attr)
        for attr in dir(cls)
        if not callable(cls().__getattribute__(attr)) and not attr.startswith("_")
    ]


def to_list(value):
    if not value:
        return []
    if not isinstance(value, (list, tuple)):
        return [value]
    return value


def parse_timestamp_to_milliseconds_precision(timestamp):
    if isinstance(timestamp, (int, float)):
        return convert_timestamp_to_str(timestamp)
    elif isinstance(timestamp, datetime):
        return convert_datetime_to_timestamp_str(timestamp)
    elif isinstance(timestamp, str):
        return convert_datetime_to_timestamp_str(
            datetime.strptime(timestamp, DATE_STR_FORMAT)
        )


def parse_timestamp_to_microseconds_precision(timestamp):
    if isinstance(timestamp, (int, float)):
        return datetime.utcfromtimestamp(timestamp).strftime(MICROSECOND_FORMAT)
    elif isinstance(timestamp, datetime):
        return timestamp.strftime(MICROSECOND_FORMAT)
    elif isinstance(timestamp, str):
        return datetime.strptime(timestamp, DATE_STR_FORMAT).strftime(
            MICROSECOND_FORMAT
        )
