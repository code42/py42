from datetime import datetime

import py42.util as util


def test_convert_timestamp_to_str_returns_expected_str():
    assert util.convert_timestamp_to_str(235123656) == "1977-06-14T08:07:36.000Z"


def test_convert_datetime_to_timestamp_str_returns_expected_str():
    d = datetime(2020, 4, 19, 13, 3, 2, 3)
    assert util.convert_datetime_to_timestamp_str(d) == "2020-04-19T13:03:02.000Z"


class TestClass:
    _private = "test"
    CONSTANT1 = "value1"
    CONSTANT2 = "value2"

    def method(self):
        pass


def test_get_attribute_keys_from_class_returns_public_class_attribute_keys():
    public_attributes = util.get_attribute_values_from_class(TestClass)
    assert set(public_attributes) == {"value1", "value2"}


def test_to_list():
    assert util.to_list(None) == []
    assert util.to_list("") == []
    assert util.to_list(["a"]) == ["a"]
    assert util.to_list("a") == ["a"]


def test_parse_timestamp_to_milliseconds_precision_returns_expected_timestamp_with_epoch_time():
    actual = util.parse_timestamp_to_milliseconds_precision(1599653541)
    assert actual == "2020-09-09T12:12:21.000Z"


def test_parse_timestamp_to_milliseconds_precision_returns_expected_timestamp_with_str_format_time():
    actual = util.parse_timestamp_to_milliseconds_precision("2020-09-09 12:12:21")
    assert actual == "2020-09-09T12:12:21.000Z"


def test_parse_timestamp_to_milliseconds_precision_when_given_unicode_returns_expected_timestamp_with_str_format_time():
    actual = util.parse_timestamp_to_milliseconds_precision("2020-09-09 12:12:21")
    assert actual == "2020-09-09T12:12:21.000Z"


def test_parse_timestamp_to_milliseconds_precision_returns_expected_timestamp_with_datetime_time():
    dt = datetime.strptime("2020-09-09 12:12:21", "%Y-%m-%d %H:%M:%S")
    actual = util.parse_timestamp_to_milliseconds_precision(dt)
    assert actual == "2020-09-09T12:12:21.000Z"


def test_parse_timestamp_to_microseconds_precision_returns_expected_timestamp_with_epoch_time():
    actual = util.parse_timestamp_to_microseconds_precision(1599653541)
    assert actual == "2020-09-09T12:12:21.000000Z"


def test_parse_timestamp_to_microseconds_precision_returns_expected_timestamp_with_str_format_time():
    actual = util.parse_timestamp_to_microseconds_precision("2020-09-09 12:12:21")
    assert actual == "2020-09-09T12:12:21.000000Z"


def test_parse_timestamp_to_microseconds_precision_when_given_unicode_returns_expected_timestamp_with_str_format_time():
    actual = util.parse_timestamp_to_microseconds_precision("2020-09-09 12:12:21")
    assert actual == "2020-09-09T12:12:21.000000Z"


def test_parse_timestamp_to_microseconds_precision_returns_expected_timestamp_with_datetime_time():
    dt = datetime.strptime("2020-09-09 12:12:21", "%Y-%m-%d %H:%M:%S")
    actual = util.parse_timestamp_to_microseconds_precision(dt)
    assert actual == "2020-09-09T12:12:21.000000Z"


def test_parse_timestamp_to_microseconds_precision_returns_expected_timestamp_with_float_time():
    actual = util.parse_timestamp_to_microseconds_precision(1599653541.001002)
    assert actual == "2020-09-09T12:12:21.001002Z"


def test_parse_timestamp_to_milliseconds_precision_returns_expected_timestamp_with_float_time():
    actual = util.parse_timestamp_to_milliseconds_precision(1599653541.001002)
    assert actual == "2020-09-09T12:12:21.001Z"
