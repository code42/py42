from __future__ import print_function

import json
from datetime import datetime


def format_json(json_string):
    """Converts a minified JSON str to a prettified JSON str.

    Args:
        json_string (str): A str representing JSON.
    """
    parsed = json.loads(json_string)
    return json.dumps(parsed, indent=4)


def print_response(response, label=None):
    """Prints a :class:`py42.sdk.response.Py42Response` as prettified JSON. If unable to
    load, it prints the given response.

    Args:
        response (:class:`py42.sdk.response.Py42Response`)
        label (str, optional): A label at the beginning of the printed text. Defaults to None.
    """
    if label:
        print(label, end=u" ")
    try:
        print(format_json(response.text))
    except ValueError:
        print(response)


def convert_timestamp_to_str(timestamp):
    """Converts the given POSIX timestamp to a date str.

    Args:
        timestamp (float): A POSIX timestamp.
    """
    date = datetime.utcfromtimestamp(timestamp)
    return convert_datetime_to_timestamp_str(date)


def convert_datetime_to_timestamp_str(date):
    """Converts the given datetime to a formatted date str.

    Args:
        date (datetime)
    """
    prefix = date.strftime(u"%Y-%m-%dT%H:%M:%S.%f")[:-3]
    return u"{0}Z".format(prefix)
