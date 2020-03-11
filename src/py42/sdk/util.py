from __future__ import print_function

import json
from datetime import datetime


def format_json(json_string):
    parsed = json.loads(json_string)
    return json.dumps(parsed, indent=4)


def print_response(response, label=None):
    if label:
        print(label, end=u" ")
    try:
        print(format_json(response.text))
    except ValueError:
        print(response)


def convert_timestamp_to_str(timestamp):
    date = datetime.utcfromtimestamp(timestamp)
    return convert_datetime_to_timestamp_str(date)


def convert_datetime_to_timestamp_str(date):
    prefix = date.strftime(u"%Y-%m-%dT%H:%M:%S.%f")[:-3]
    return u"{0}Z".format(prefix)
