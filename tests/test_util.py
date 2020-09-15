from datetime import datetime

import pytest

import py42.util as util


def test_convert_timestamp_to_str_returns_expected_str():
    assert util.convert_timestamp_to_str(235123656) == "1977-06-14T08:07:36.000Z"


def test_convert_datetime_to_timestamp_str_returns_expected_str():
    d = datetime(2020, 4, 19, 13, 3, 2, 3)
    assert util.convert_datetime_to_timestamp_str(d) == "2020-04-19T13:03:02.000Z"


class TestClass(object):
    _private = "test"
    CONSTANT1 = "value1"
    CONSTANT2 = "value2"

    def method(self):
        pass


def test_get_attribute_keys_from_class_returns_public_class_attribute_keys():
    public_attributes = util.get_attribute_keys_from_class(TestClass)
    assert set(public_attributes) == {"value1", "value2"}


def test_to_list():
    assert util.to_list(None) == []
    assert util.to_list("") == []
    assert util.to_list(["a"]) == ["a"]
    assert util.to_list(tuple("a")) == ["a"]


def test_to_list_raises_exception_when_type_conversion_is_not_supported():
    with pytest.raises(ValueError) as ex:
        util.to_list({"a": "b"})

    assert "Can't convert type <class 'dict'> to list type" in str(ex.value)

    with pytest.raises(ValueError) as ex:
        util.to_list({1, 2})
    assert "Can't convert type <class 'set'> to list type" in str(ex.value)
