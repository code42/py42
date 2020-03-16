from datetime import datetime

import py42._internal.session
import py42.sdk.util as util


def test_convert_timestamp_to_str_returns_expected_str():
    assert util.convert_timestamp_to_str(235123656) == "1977-06-14T08:07:36.000Z"


def test_convert_datetime_to_timestamp_str_returns_expected_str():
    d = datetime(2020, 4, 19, 13, 3, 2, 3)
    assert util.convert_datetime_to_timestamp_str(d) == "2020-04-19T13:03:02.000Z"
