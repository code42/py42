from __future__ import print_function

import json
from datetime import datetime


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
        print(label, end=u" ")
    try:
        print(format_json(response.text))
    except ValueError:
        print(response)


def convert_timestamp_to_str(timestamp):
    """Converts the given POSIX timestamp to a date str. The format matches strftime
    directives %Y-%m-%dT%H:%M:%S.%f.

    Args:
        timestamp (float): A POSIX timestamp.

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
    prefix = date.strftime(u"%Y-%m-%dT%H:%M:%S.%f")[:-3]
    return u"{0}Z".format(prefix)


def convert_datetime_to_epoch(date):
    return (date - datetime.utcfromtimestamp(0)).total_seconds()
