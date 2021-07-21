from tests.sdk.queries.conftest import IS
from tests.sdk.queries.conftest import IS_IN
from tests.sdk.queries.conftest import IS_NOT
from tests.sdk.queries.conftest import NOT_IN

from py42.sdk.queries.fileevents.filters.risk_filter import RiskIndicator, RiskSeverity


def test_risk_indicator_eq_str_gives_correct_json_representation():
    _filter = RiskIndicator.eq(RiskIndicator.CloudDataExposures.PUBLIC_CORPORATE_BOX)
    expected = IS.format("riskIndicatorNames", "Public link from corporate Box")
    assert str(_filter) == expected


def test_risk_indicator_not_eq_str_gives_correct_json_representation():
    _filter = RiskIndicator.not_eq(RiskIndicator.CloudStorageUploads.AMAZON_DRIVE)
    expected = IS_NOT.format("riskIndicatorNames", "Amazon Drive upload")
    assert str(_filter) == expected


def test_risk_indicator_is_in_str_gives_correct_json_representation():
    items = [RiskIndicator.FileCategories.EXECUTABLE, RiskIndicator.FileCategories.IMAGE, RiskIndicator.FileCategories.PDF]
    _filter = RiskIndicator.is_in(items)
    expected = IS_IN.format("riskIndicatorNames", *items)
    assert str(_filter) == expected


def test_risk_indicator_not_in_str_gives_correct_json_representation():
    items = [RiskIndicator.FileCategories.EXECUTABLE, RiskIndicator.FileCategories.IMAGE, RiskIndicator.FileCategories.PDF]
    _filter = RiskIndicator.not_in(items)
    expected = NOT_IN.format("riskIndicatorNames", *items)
    assert str(_filter) == expected


def test_risk_severity_eq_str_gives_correct_json_representation():
    _filter = RiskSeverity.eq(RiskSeverity.HIGH)
    expected = IS.format("riskSeverity", "HIGH")
    assert str(_filter) == expected


def test_risk_severity_not_eq_str_gives_correct_json_representation():
    _filter = RiskSeverity.not_eq(RiskSeverity.CRITICAL)
    expected = IS_NOT.format("riskSeverity", "CRITICAL")
    assert str(_filter) == expected


def test_risk_severity_is_in_str_gives_correct_json_representation():
    items = [RiskSeverity.HIGH, RiskSeverity.LOW, RiskSeverity.MODERATE]
    _filter = RiskSeverity.is_in(items)
    expected = IS_IN.format("riskSeverity", *items)
    assert str(_filter) == expected


def test_risk_severity_not_in_str_gives_correct_json_representation():
    items = [RiskSeverity.HIGH, RiskSeverity.LOW, RiskSeverity.MODERATE]
    _filter = RiskSeverity.not_in(items)
    expected = NOT_IN.format("riskSeverity", *items)
    assert str(_filter) == expected
