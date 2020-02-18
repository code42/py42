from __future__ import print_function

import json
import os
import posixpath
from datetime import datetime

from requests import Response


def get_obj_from_response(response, data_key):
    if response.text and 200 <= response.status_code < 300:
        response_json = json.loads(response.text)
        if u"data" in response_json:
            data = response_json[u"data"]
            if data_key == u"data":
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
        print(label, end=u" ")
    try:
        print(format_json(response.text))
    except ValueError:
        print(response)


def print_response_data(response, label=None):
    try:
        print_dict(get_obj_from_response(response, u"data"), label=label)
    except ValueError:
        print(response)


def print_dict(dict_, label=None):
    if label:
        print(label, end=" ")
    print(json.dumps(dict_, indent=4))


def verify_path_writeable(path):
    # If the file exists, see if we can overwrite it.
    if posixpath.exists(path):
        if not os.access(path, os.W_OK):
            raise IOError(u"Insufficient permissions to write to file: {0}".format(path))
    else:
        # Otherwise see if we can write to the directory (assuming it already exists)
        directory = posixpath.dirname(path)
        if not posixpath.exists(directory):
            raise IOError(u"Directory does not exist: {0}".format(directory))
        if not os.access(directory, os.W_OK):
            raise IOError(u"Insufficient permissions to write to directory: {0}".format(directory))
    return path


def build_path(filename, directory=None, default_dir=posixpath.curdir):
    if not directory:
        directory = default_dir
    return posixpath.join(directory, filename)


def save_content_to_disk(response, file_path):
    # type: (Response, str) -> None
    """Saves the content of a Response to disk at the given path

    Args:
        response: a Response object with content
        file_path: absolute path to which the content will be written

    Raises:
        IOError: if the current user does not have permission to write to file_path or an IO error occurs trying
            to write the content to the file
    """
    with open(file_path, u"wb") as fd:
        for chunk in response.iter_content(chunk_size=128):
            fd.write(chunk)


def filter_out_none(_dict):
    # type: (dict) -> dict
    return {key: _dict[key] for key in _dict if _dict[key] is not None}


def convert_timestamp_to_str(timestamp):
    date = datetime.utcfromtimestamp(timestamp)
    return convert_datetime_to_timestamp_str(date)


def convert_datetime_to_timestamp_str(date):
    prefix = date.strftime(u"%Y-%m-%dT%H:%M:%S.%f")[:-3]
    return u"{0}Z".format(prefix)
