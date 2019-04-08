from __future__ import print_function

import json


def wrap_func(func, existing_func):
    def wrapped(*args, **kwargs):
        if existing_func is not None:
            existing_func(*args, **kwargs)
        func(*args, **kwargs)
    return wrapped


def get_obj_from_response(response, data_key):
    if response.content and 200 <= response.status_code < 300:
        response_json = json.loads(response.content)
        if "data" in response_json:
            data = response_json["data"]
            if data_key == "data":
                return data
            if data_key in data:
                return data[data_key]
    else:
        return []


def format_json(json_string):
    parsed = json.loads(json_string)
    return json.dumps(parsed, indent=4)


def print_response(response, label=None):
    if label:
        print(label, end=' ')
    try:
        print(format_json(response.content))
    except ValueError:
        print(response)


def print_dict(dict_, label=None):
    if label:
        print(label, end=' ')
    print(json.dumps(dict_, indent=4))
