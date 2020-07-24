from py42.sdk.queries.fileevents.filters.activity_filter import RemoteActivity
from py42.sdk.queries.fileevents.filters.activity_filter import TrustedActivity

from tests.sdk.queries.conftest import IS


def test_risk_indicator_mime_type_is_true_str_gives_correct_json_representation():
    _filter = RemoteActivity.is_true()
    expected = IS.format("remoteActivity", "TRUE")
    assert str(_filter) == expected


def test_risk_indicator_mime_type_is_false_str_gives_correct_json_representation():
    _filter = RemoteActivity.is_false()
    expected = IS.format("remoteActivity", "FALSE")
    assert str(_filter) == expected


def test_risk_indicator_active_hours_is_true_str_gives_correct_json_representation():
    _filter = TrustedActivity.is_true()
    expected = IS.format("trusted", "TRUE")
    assert str(_filter) == expected


def test_risk_indicator_active_hours_is_false_str_gives_correct_json_representation():
    _filter = TrustedActivity.is_false()
    expected = IS.format("trusted", "FALSE")
    assert str(_filter) == expected
