from datetime import datetime

import py42.util as util
from py42.util import filter_attributes


def test_convert_timestamp_to_str_returns_expected_str():
    assert util.convert_timestamp_to_str(235123656) == "1977-06-14T08:07:36.000Z"


def test_convert_datetime_to_timestamp_str_returns_expected_str():
    d = datetime(2020, 4, 19, 13, 3, 2, 3)
    assert util.convert_datetime_to_timestamp_str(d) == "2020-04-19T13:03:02.000Z"


class FilterClassTest(object):
    _private = "test"
    CONSTANT1 = "value1"
    CONSTANT2 = "value2"

    def method(self):
        pass


def test_filter_attributes_returns_public_class_variables():
    public_attributes = filter_attributes(FilterClassTest)
    assert set(public_attributes) == {"value1", "value2"}
