import pytest

from py42.sdk.queries.fileevents.filters.print_filter import Printer
from py42.sdk.queries.fileevents.filters.print_filter import PrintJobName

from tests.sdk.queries.conftest import IS
from tests.sdk.queries.conftest import IS_NOT
from tests.sdk.queries.conftest import IS_IN
from tests.sdk.queries.conftest import NOT_IN


@pytest.mark.parametrize(
    "filter_criteria, test_filter",
    [(Printer.eq, IS), (Printer.not_eq, IS_NOT)],
)
def test_equality_device_signed_in_username_gives_correct_json_representation(
    filter_criteria, test_filter
):
    _filter = filter_criteria("printer")
    expected = test_filter.format("printerName", "printer")
    assert str(_filter) == expected


@pytest.mark.parametrize(
    "filter_criteria, test_filter",
    [(Printer.is_in, IS_IN), (Printer.not_in, NOT_IN)],
)
def test_multi_vlaue_device_signed_in_username_gives_correct_json_representation(
    filter_criteria, test_filter
):
    usernames = ["printer1", "printer2", "printer3"]
    _filter = filter_criteria(usernames)
    expected = test_filter.format("printerName", *usernames)
    assert str(_filter) == expected


@pytest.mark.parametrize(
    "filter_criteria, test_filter",
    [(PrintJobName.eq, IS), (PrintJobName.not_eq, IS_NOT)],
)
def test_equality_device_signed_in_username_gives_correct_json_representation(
    filter_criteria, test_filter
):
    _filter = filter_criteria("job")
    expected = test_filter.format("printJobName", "job")
    assert str(_filter) == expected


@pytest.mark.parametrize(
    "filter_criteria, test_filter",
    [(PrintJobName.is_in, IS_IN), (PrintJobName.not_in, NOT_IN)],
)
def test_multi_vlaue_device_signed_in_username_gives_correct_json_representation(
    filter_criteria, test_filter
):
    usernames = ["job1", "job2", "job3"]
    _filter = filter_criteria(usernames)
    expected = test_filter.format("printJobName", *usernames)
    assert str(_filter) == expected
