# -*- coding: utf-8 -*-

import os
from datetime import datetime

import pytest
from requests import Response

import py42._internal.compat as compat
import py42.sdk.util as util

TEST_FILENAME = "file.txt"
TEST_DIR = "/Users/john.doe"
TEST_PATH = "{0}/{1}".format(TEST_DIR, TEST_FILENAME)
TEST_UNICODE_FILENAME = u"文件"
TEST_UNICODE_DIR = u"夹"
TEST_UNICODE_PATH = u"{0}/{1}".format(TEST_UNICODE_DIR, TEST_UNICODE_FILENAME)
BUILTIN_MODULE = "__builtin__" if compat.is_py2 else "builtins"


def mock_access(can_access=True):
    def access(path, int):
        return can_access

    return access


def mock_dir_only_access():
    def access(path, int):
        return path == TEST_DIR and int == os.W_OK

    return access


@pytest.fixture
def non_existing_dir(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda path: False)
    monkeypatch.setattr("os.access", mock_access(False))
    return TEST_PATH


@pytest.fixture
def non_existent_unicode_dir(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda path: False)
    monkeypatch.setattr("os.access", mock_access(False))
    return TEST_UNICODE_PATH


@pytest.fixture
def existing_dir_not_writeable(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda path: path == TEST_DIR)
    monkeypatch.setattr("os.access", mock_access(False))
    return TEST_PATH


@pytest.fixture
def existing_unicode_dir_not_writeable(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda path: path == TEST_UNICODE_DIR)
    monkeypatch.setattr("os.access", mock_access(False))
    return TEST_UNICODE_PATH


@pytest.fixture
def non_existing_file_writeable(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda path: path == TEST_DIR)
    monkeypatch.setattr("os.access", mock_access())
    return TEST_PATH


@pytest.fixture
def existing_file_writeable(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda path: True)
    monkeypatch.setattr("os.access", mock_access())
    return TEST_PATH


@pytest.fixture
def existing_file_not_writeable(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda path: True)
    monkeypatch.setattr("os.access", mock_dir_only_access())
    return TEST_PATH


@pytest.fixture
def existing_unicode_file_not_writeable(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda path: True)
    monkeypatch.setattr("os.access", mock_dir_only_access())
    return TEST_UNICODE_PATH


@pytest.fixture
def mock_open(mocker):
    mock_open = mocker.MagicMock()
    mocker.mock_open(mock_open)
    return mocker.patch("{0}{1}".format(BUILTIN_MODULE, ".open"), mock_open)


@pytest.fixture
def response(mocker):
    return mocker.MagicMock(spec=Response)


@pytest.fixture
def response_content():
    return "content"


def test_verify_path_writeable_if_dir_not_exists_raises_io_error(non_existing_dir):
    with pytest.raises(Exception) as e:
        util.verify_path_writeable(non_existing_dir)
    assert e.type == IOError
    assert e.value.args[0] == u"Directory does not exist: {0}".format(TEST_DIR)


def test_verify_path_writeable_if_unicode_dir_not_exists_raises_io_error(non_existent_unicode_dir):
    with pytest.raises(Exception) as e:
        util.verify_path_writeable(non_existent_unicode_dir)
    assert e.type == IOError
    assert e.value.args[0] == u"Directory does not exist: {0}".format(TEST_UNICODE_DIR)


def test_verify_path_writeable_if_dir_not_writeable_raises_io_error(existing_dir_not_writeable):
    with pytest.raises(Exception) as e:
        util.verify_path_writeable(existing_dir_not_writeable)
    assert e.type == IOError
    assert e.value.args[0] == u"Insufficient permissions to write to directory: {0}".format(
        TEST_DIR
    )


def test_verify_path_writeable_if_unicode_dir_not_writeable_raises_io_error(
    existing_unicode_dir_not_writeable,
):
    with pytest.raises(Exception) as e:
        util.verify_path_writeable(existing_unicode_dir_not_writeable)
    assert e.type == IOError
    assert e.value.args[0] == u"Insufficient permissions to write to directory: {0}".format(
        TEST_UNICODE_DIR
    )


def test_verify_path_writeable_if_file_not_writeable_raises_io_error(existing_file_not_writeable):
    with pytest.raises(Exception) as e:
        util.verify_path_writeable(existing_file_not_writeable)
    assert e.type == IOError
    assert e.value.args[0] == u"Insufficient permissions to write to file: {0}".format(
        existing_file_not_writeable
    )


def test_verify_path_writeable_if_unicode_file_not_writeable_raises_io_error(
    existing_unicode_file_not_writeable,
):
    with pytest.raises(Exception) as e:
        util.verify_path_writeable(existing_unicode_file_not_writeable)
    assert e.type == IOError
    assert e.value.args[0] == u"Insufficient permissions to write to file: {0}".format(
        existing_unicode_file_not_writeable
    )


def test_verify_path_writeable_when_existing_file_writeable_returns_path(existing_file_writeable):
    path = util.verify_path_writeable(existing_file_writeable)
    assert path == existing_file_writeable


def test_verify_path_writeable_when_non_existing_file_writeable_returns_path(
    non_existing_file_writeable,
):
    path = util.verify_path_writeable(non_existing_file_writeable)
    assert path == non_existing_file_writeable


def test_build_path_with_filename_returns_path_with_curdir():
    path = util.build_path(TEST_FILENAME)
    assert path == "./{0}".format(TEST_FILENAME)


def test_build_path_with_filename_and_save_as_dir_returns_path_with_save_as_dir():
    path = util.build_path(TEST_FILENAME, directory=TEST_DIR)
    assert path == "{0}/{1}".format(TEST_DIR, TEST_FILENAME)


def test_build_path_with_filename_and_none_save_as_dir_returns_path_with_curdir():
    path = util.build_path(TEST_FILENAME, directory=None)
    assert path == "./{0}".format(TEST_FILENAME)


def test_build_path_with_filename_none_save_as_dir_and_custom_default_dir_returns_path_with_default_dir():
    path = util.build_path(TEST_FILENAME, directory=None, default_dir="/temp")
    assert path == "/temp/{0}".format(TEST_FILENAME)


def test_save_content_to_disk_opens_file_at_given_path(
    mocker, mock_open, response, response_content
):
    response.iter_content.return_value = list(response_content)
    util.save_content_to_disk(response, TEST_PATH)
    mock_open.assert_called_once_with(TEST_PATH, mocker.ANY)


def test_save_content_to_disk_opens_file_in_binary_mode(
    mocker, mock_open, response, response_content
):
    response.iter_content.return_value = list(response_content)
    util.save_content_to_disk(response, TEST_PATH)
    mock_open.assert_called_once_with(mocker.ANY, "wb")


def test_save_content_to_disk_opens_file_once(mock_open, response, response_content):
    response.iter_content.return_value = list(response_content)
    util.save_content_to_disk(response, TEST_PATH)
    assert mock_open.call_count == 1


def test_save_content_to_disk_uses_context_manager(mock_open, response):
    # util.save_content_to_disk uses a context manager. Using 'with' here with mock_open will fail if the open being
    # mocked isn't called within the context of a context manager
    with mock_open:
        util.save_content_to_disk(response, TEST_PATH)


def test_save_content_to_disk_calls_write_for_each_content_chunk(
    mock_open, response, response_content
):
    response.iter_content.return_value = list(response_content)
    util.save_content_to_disk(response, TEST_PATH)
    assert mock_open.return_value.write.call_count == len(response_content)


def test_save_content_to_disk_calls_write_with_the_correct_content(
    mocker, mock_open, response, response_content
):
    response.iter_content.return_value = list(response_content)
    util.save_content_to_disk(response, TEST_PATH)
    expected_calls = [mocker.call(chunk) for chunk in response_content]
    mock_open.return_value.write.assert_has_calls(expected_calls)


def test_save_content_to_disk_raises_exception_when_open_raises_exception(mock_open, response):
    message = "Error opening file!"
    mock_open.side_effect = IOError(message)
    with pytest.raises(IOError) as e:
        util.save_content_to_disk(response, TEST_PATH)
    assert e.value.args[0] == message


def test_filter_out_none_given_empty_dict_returns_empty_dict():
    assert util.filter_out_none({}) == {}


def test_filter_out_none_given_dict_with_one_non_none_element_returns_dict_with_the_non_none_element():
    assert util.filter_out_none({"one": 1}) == {"one": 1}


def test_filter_out_none_given_dict_with_one_none_element_returns_empty_dict():
    assert util.filter_out_none({"one": None}) == {}


def test_filter_out_none_given_dict_with_two_non_none_elements_returns_dict_with_the_non_none_elements():
    assert util.filter_out_none({"one": 1, "two": 2}) == {"one": 1, "two": 2}


def test_filter_out_none_given_dict_with_two_none_elements_returns_empty_dict():
    assert util.filter_out_none({"one": None, "two": None}) == {}


def test_filter_out_none_given_dict_with_one_non_none_and_two_none_returns_dict_with_the_one_non_none_element():
    assert util.filter_out_none({"one": 1, "two": None, "three": None}) == {"one": 1}


def test_filter_out_none_given_dict_with_two_non_none_and_one_none_returns_dict_with_the_two_non_none_elements():
    assert util.filter_out_none({"one": 1, "two": 2, "three": None}) == {"one": 1, "two": 2}


def test_filter_out_none_given_dict_with_two_non_none_and_two_none_returns_dict_with_the_two_non_none_elements():
    d = {"one": 1, "two": 2, "three": None, "four": None}
    assert util.filter_out_none(d) == {"one": 1, "two": 2}


def test_filter_out_none_does_not_filter_out_empty_string_value():
    assert util.filter_out_none({"empty": ""}) == {"empty": ""}


def test_filter_out_none_does_not_filter_out_empty_list():
    assert util.filter_out_none({"empty-list": []}) == {"empty-list": []}


def test_filter_out_none_does_not_filter_out_zero():
    assert util.filter_out_none({"zero": 0}) == {"zero": 0}


def test_filter_out_none_does_not_filter_out_false():
    assert util.filter_out_none({"false": False}) == {"false": False}


def test_filter_out_none_does_not_filter_out_empty_tuple():
    assert util.filter_out_none({"empty-tuple": ()}) == {"empty-tuple": ()}


def test_convert_timestamp_to_str_returns_expected_str():
    assert util.convert_timestamp_to_str(235123656) == "1977-06-14T08:07:36.000Z"


def test_convert_datetime_to_timestamp_str_returns_expected_str():
    d = datetime(2020, 4, 19, 13, 3, 2, 3)
    assert util.convert_datetime_to_timestamp_str(d) == "2020-04-19T13:03:02.000Z"
