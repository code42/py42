from tests.sdk.queries.conftest import GREATER_THAN
from tests.sdk.queries.conftest import IS
from tests.sdk.queries.conftest import IS_IN
from tests.sdk.queries.conftest import IS_NOT
from tests.sdk.queries.conftest import LESS_THAN
from tests.sdk.queries.conftest import NOT_IN

from py42.sdk.queries.fileevents.v2.filters.risk_filter import RiskIndicator, \
    TrustedActivity, TrustReason
from py42.sdk.queries.fileevents.v2.filters.risk_filter import RiskScore
from py42.sdk.queries.fileevents.v2.filters.risk_filter import RiskSeverity


def test_risk_indicator_eq_str_gives_correct_json_representation():
    _filter = RiskIndicator.eq(RiskIndicator.CloudDataExposures.PUBLIC_CORPORATE_BOX)
    expected = IS.format("risk.indicators.name", "Public link from corporate Box")
    assert str(_filter) == expected


def test_risk_indicator_not_eq_str_gives_correct_json_representation():
    _filter = RiskIndicator.not_eq(RiskIndicator.CloudStorageUploads.AMAZON_DRIVE)
    expected = IS_NOT.format("risk.indicators.name", "Amazon Drive upload")
    assert str(_filter) == expected


def test_risk_indicator_is_in_str_gives_correct_json_representation():
    items = [
        RiskIndicator.FileCategories.EXECUTABLE,
        RiskIndicator.FileCategories.IMAGE,
        RiskIndicator.FileCategories.PDF,
    ]
    _filter = RiskIndicator.is_in(items)
    expected = IS_IN.format("risk.indicators.name", *items)
    assert str(_filter) == expected


def test_risk_indicator_not_in_str_gives_correct_json_representation():
    items = [
        RiskIndicator.FileCategories.EXECUTABLE,
        RiskIndicator.FileCategories.IMAGE,
        RiskIndicator.FileCategories.PDF,
    ]
    _filter = RiskIndicator.not_in(items)
    expected = NOT_IN.format("risk.indicators.name", *items)
    assert str(_filter) == expected


def test_risk_severity_eq_str_gives_correct_json_representation():
    _filter = RiskSeverity.eq(RiskSeverity.HIGH)
    expected = IS.format("risk.severity", "HIGH")
    assert str(_filter) == expected


def test_risk_severity_not_eq_str_gives_correct_json_representation():
    _filter = RiskSeverity.not_eq(RiskSeverity.CRITICAL)
    expected = IS_NOT.format("risk.severity", "CRITICAL")
    assert str(_filter) == expected


def test_risk_severity_is_in_str_gives_correct_json_representation():
    items = [RiskSeverity.HIGH, RiskSeverity.LOW, RiskSeverity.MODERATE]
    _filter = RiskSeverity.is_in(items)
    expected = IS_IN.format("risk.severity", *items)
    assert str(_filter) == expected


def test_risk_severity_not_in_str_gives_correct_json_representation():
    items = [RiskSeverity.HIGH, RiskSeverity.LOW, RiskSeverity.MODERATE]
    _filter = RiskSeverity.not_in(items)
    expected = NOT_IN.format("risk.severity", *items)
    assert str(_filter) == expected


def test_risk_score_eq_str_gives_correct_json_representation():
    _filter = RiskScore.eq(5)
    expected = IS.format("risk.score", "5")
    assert str(_filter) == expected


def test_risk_score_not_eq_str_gives_correct_json_representation():
    _filter = RiskScore.not_eq(5)
    expected = IS_NOT.format("risk.score", "5")
    assert str(_filter) == expected


def test_risk_score_is_in_str_gives_correct_json_representation():
    items = [3, 4, 5]
    _filter = RiskScore.is_in(items)
    expected = IS_IN.format("risk.score", *items)
    assert str(_filter) == expected


def test_risk_score_not_in_str_gives_correct_json_representation():
    items = [3, 4, 5]
    _filter = RiskScore.not_in(items)
    expected = NOT_IN.format("risk.score", *items)
    assert str(_filter) == expected


def test_risk_score_greater_than_str_gives_correct_json_representation():
    _filter = RiskScore.greater_than(5)
    expected = GREATER_THAN.format("risk.score", "5")
    assert str(_filter) == expected


def test_risk_score_less_than_str_gives_correct_json_representation():
    _filter = RiskScore.less_than(5)
    expected = LESS_THAN.format("risk.score", "5")
    assert str(_filter) == expected


def test_risk_indicator_active_hours_is_true_str_gives_correct_json_representation():
    _filter = TrustedActivity.is_true()
    expected = IS.format("risk.trusted", "TRUE")
    assert str(_filter) == expected


def test_risk_indicator_active_hours_is_false_str_gives_correct_json_representation():
    _filter = TrustedActivity.is_false()
    expected = IS.format("risk.trusted", "FALSE")
    assert str(_filter) == expected


def test_trust_reason_eq_str_gives_correct_json_representation():
    _filter = TrustReason.eq("")  # TODO
    expected = IS.format("risk.trustReason", "")
    assert str(_filter) == expected


def test_trust_reason_not_eq_str_gives_correct_json_representation():
    _filter = TrustReason.not_eq("")
    expected = IS_NOT.format("risk.trustReason", "")
    assert str(_filter) == expected


def test_trust_reason_is_in_str_gives_correct_json_representation():
    items = []  # TODO
    _filter = TrustReason.is_in(items)
    expected = IS_IN.format("risk.trustReason", *items)
    assert str(_filter) == expected


def test_trust_reason_not_in_str_gives_correct_json_representation():
    items = []  # TODO
    _filter = TrustReason.not_in(items)
    expected = NOT_IN.format("risk.trustReason", *items)
    assert str(_filter) == expected

