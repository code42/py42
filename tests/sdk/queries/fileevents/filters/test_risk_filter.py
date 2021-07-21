from tests.sdk.queries.conftest import IS
from tests.sdk.queries.conftest import IS_IN
from tests.sdk.queries.conftest import IS_NOT
from tests.sdk.queries.conftest import NOT_IN

from py42.sdk.queries.fileevents.filters.risk_filter import RiskIndicator, RiskSeverity


def test_risk_indicator_eq_str_gives_correct_json_representation():
    _filter = RiskIndicator.eq(RiskIndicator.CloudDataExposures.PUBLIC_CORPORATE_BOX)
    expected = IS.format("riskIndicators", "Public link from corporate Box")
    assert str(_filter) == expected


def test_risk_indicator_not_eq_str_gives_correct_json_representation():
    _filter = RiskIndicator.not_eq(RiskIndicator.CloudStorageUploads.AMAZON_DRIVE)
    expected = IS_NOT.format("riskIndicators", "Amazon Drive upload")
    assert str(_filter) == expected


def test_risk_indicator_is_in_str_gives_correct_json_representation():
    items = [RiskIndicator.FileCategories.EXECUTABLE, RiskIndicator.FileCategories.IMAGE, RiskIndicator.FileCategories.PDF]
    _filter = RiskIndicator.is_in(items)
    expected = IS_IN.format("riskIndicators", *items)
    assert str(_filter) == expected


def test_risk_indicator_not_in_str_gives_correct_json_representation():
    items = [RiskIndicator.FileCategories.EXECUTABLE, RiskIndicator.FileCategories.IMAGE, RiskIndicator.FileCategories.PDF]
    _filter = RiskIndicator.not_in(items)
    expected = NOT_IN.format("riskIndicators", *items)
    assert str(_filter) == expected


def test_risk_severity_eq_str_gives_correct_json_representation():
    _filter = RiskIndicator.eq(RiskIndicator.CloudDataExposures.PUBLIC_CORPORATE_BOX)
    expected = IS.format("riskIndicators", "Public link from corporate Box")
    assert str(_filter) == expected


def test_risk_severity_not_eq_str_gives_correct_json_representation():
    _filter = RiskIndicator.not_eq(RiskIndicator.CloudStorageUploads.AMAZON_DRIVE)
    expected = IS_NOT.format("riskIndicators", "Amazon Drive upload")
    assert str(_filter) == expected


def test_risk_severity_is_in_str_gives_correct_json_representation():
    items = [RiskIndicator.FileCategories.EXECUTABLE, RiskIndicator.FileCategories.IMAGE, RiskIndicator.FileCategories.PDF]
    _filter = RiskIndicator.is_in(items)
    expected = IS_IN.format("riskIndicators", *items)
    assert str(_filter) == expected


def test_risk_severity_not_in_str_gives_correct_json_representation():
    items = [RiskIndicator.FileCategories.EXECUTABLE, RiskIndicator.FileCategories.IMAGE, RiskIndicator.FileCategories.PDF]
    _filter = RiskIndicator.not_in(items)
    expected = NOT_IN.format("riskIndicators", *items)
    assert str(_filter) == expected
