from datetime import datetime
from time import time

import pytest
from tests.sdk.queries.conftest import EXISTS
from tests.sdk.queries.conftest import format_datetime
from tests.sdk.queries.conftest import format_timestamp
from tests.sdk.queries.conftest import IN_RANGE
from tests.sdk.queries.conftest import IS
from tests.sdk.queries.conftest import IS_IN
from tests.sdk.queries.conftest import IS_NOT
from tests.sdk.queries.conftest import NOT_EXISTS
from tests.sdk.queries.conftest import NOT_IN
from tests.sdk.queries.conftest import ON_OR_AFTER
from tests.sdk.queries.conftest import ON_OR_BEFORE
from tests.sdk.queries.conftest import WITHIN_THE_LAST

from py42.sdk.queries.fileevents.filters.event_filter import EventTimestamp
from py42.sdk.queries.fileevents.filters.event_filter import EventType
from py42.sdk.queries.fileevents.filters.event_filter import InsertionTimestamp
from py42.sdk.queries.fileevents.filters.event_filter import MimeTypeMismatch
from py42.sdk.queries.fileevents.filters.event_filter import OutsideActiveHours
from py42.sdk.queries.fileevents.filters.event_filter import Source


def test_event_timestamp_filter_has_within_the_last():
    assert hasattr(EventTimestamp(), "within_the_last")


def test_insertion_timestamp_filter_has_within_the_last():
    assert hasattr(InsertionTimestamp(), "within_the_last")


def test_event_timestamp_on_or_after_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = EventTimestamp.on_or_after(test_time)
    expected = ON_OR_AFTER.format("eventTimestamp", formatted)
    assert str(_filter) == expected


def test_event_timestamp_on_or_before_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = EventTimestamp.on_or_before(test_time)
    expected = ON_OR_BEFORE.format("eventTimestamp", formatted)
    assert str(_filter) == expected


def test_event_timestamp_in_range_str_gives_correct_json_representation():
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = format_timestamp(test_before_time)
    formatted_after = format_timestamp(test_after_time)
    _filter = EventTimestamp.in_range(test_before_time, test_after_time)
    expected = IN_RANGE.format("eventTimestamp", formatted_before, formatted_after)
    assert str(_filter) == expected


def test_event_timestamp_on_same_day_str_gives_correct_json_representation():
    test_time = time()
    test_date = datetime.utcfromtimestamp(test_time)
    start_time = datetime(test_date.year, test_date.month, test_date.day, 0, 0, 0)
    end_time = datetime(test_date.year, test_date.month, test_date.day, 23, 59, 59)
    formatted_before = format_datetime(start_time)
    formatted_after = format_datetime(end_time)

    _filter = EventTimestamp.on_same_day(test_time)
    expected = IN_RANGE.format("eventTimestamp", formatted_before, formatted_after)
    assert str(_filter) == expected


def test_event_type_exists_str_gives_correct_json_representation():
    _filter = EventType.exists()
    expected = EXISTS.format("eventType")
    assert str(_filter) == expected


def test_event_type_not_exists_str_gives_correct_json_representation():
    _filter = EventType.not_exists()
    expected = NOT_EXISTS.format("eventType")
    assert str(_filter) == expected


def test_event_type_eq_str_gives_correct_json_representation():
    _filter = EventType.eq(EventType.MODIFIED)
    expected = IS.format("eventType", "MODIFIED")
    assert str(_filter) == expected


def test_event_type_not_eq_str_gives_correct_json_representation():
    _filter = EventType.not_eq(EventType.CREATED)
    expected = IS_NOT.format("eventType", "CREATED")
    assert str(_filter) == expected


def test_event_type_is_in_str_gives_correct_json_representation():
    items = [EventType.DELETED, EventType.EMAILED, EventType.PRINTED]
    _filter = EventType.is_in(items)
    expected = IS_IN.format("eventType", *items)
    assert str(_filter) == expected


def test_event_type_not_in_str_gives_correct_json_representation():
    items = [EventType.CREATED, EventType.DELETED, EventType.MODIFIED]
    _filter = EventType.not_in(items)
    expected = NOT_IN.format("eventType", *items)
    assert str(_filter) == expected


def test_insertion_timestamp_on_or_after_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = InsertionTimestamp.on_or_after(test_time)
    expected = ON_OR_AFTER.format("insertionTimestamp", formatted)

    assert str(_filter) == expected


def test_insertion_timestamp_on_or_before_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = InsertionTimestamp.on_or_before(test_time)
    expected = ON_OR_BEFORE.format("insertionTimestamp", formatted)
    assert str(_filter) == expected


def test_insertion_timestamp_in_range_str_gives_correct_json_representation():
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = format_timestamp(test_before_time)
    formatted_after = format_timestamp(test_after_time)
    _filter = InsertionTimestamp.in_range(test_before_time, test_after_time)
    expected = IN_RANGE.format("insertionTimestamp", formatted_before, formatted_after)
    assert str(_filter) == expected


def test_insertion_timestamp_on_same_day_str_gives_correct_json_representation():
    test_time = time()
    test_date = datetime.utcfromtimestamp(test_time)
    start_time = datetime(test_date.year, test_date.month, test_date.day, 0, 0, 0)
    end_time = datetime(test_date.year, test_date.month, test_date.day, 23, 59, 59)
    formatted_before = format_datetime(start_time)
    formatted_after = format_datetime(end_time)
    _filter = InsertionTimestamp.on_same_day(test_time)
    expected = IN_RANGE.format("insertionTimestamp", formatted_before, formatted_after)
    assert str(_filter) == expected


def test_source_exists_str_gives_correct_json_representation():
    _filter = Source.exists()
    expected = EXISTS.format("source")
    assert str(_filter) == expected


def test_source_not_exists_str_gives_correct_json_representation():
    _filter = Source.not_exists()
    expected = NOT_EXISTS.format("source")
    assert str(_filter) == expected


def test_source_eq_str_gives_correct_json_representation():
    _filter = Source.eq(Source.ENDPOINT)
    expected = IS.format("source", "Endpoint")
    assert str(_filter) == expected


def test_source_not_eq_str_gives_correct_json_representation():
    _filter = Source.not_eq(Source.BOX)
    expected = IS_NOT.format("source", "Box")
    assert str(_filter) == expected


def test_source_is_in_str_gives_correct_json_representation():
    items = [Source.GMAIL, Source.GOOGLE_DRIVE, Source.OFFICE_365]
    _filter = Source.is_in(items)
    expected = IS_IN.format("source", *items)
    assert str(_filter) == expected


def test_source_not_in_str_gives_correct_json_representation():
    items = [Source.GMAIL, Source.GOOGLE_DRIVE, Source.OFFICE_365]
    _filter = Source.not_in(items)
    expected = NOT_IN.format("source", *items)
    assert str(_filter) == expected


def test_event_timestamp_choices_returns_valid_set():
    choices = EventTimestamp.choices()
    valid_set = {
        "PT15M",
        "PT1H",
        "PT3H",
        "PT12H",
        "P1D",
        "P3D",
        "P7D",
        "P14D",
        "P30D",
    }
    assert set(choices) == valid_set


def test_event_type_choices_returns_valid_set():
    choices = EventType.choices()
    valid_set = {
        "CREATED",
        "MODIFIED",
        "DELETED",
        "READ_BY_APP",
        "EMAILED",
        "PRINTED",
    }
    assert set(choices) == valid_set


def test_source_choices_returns_valid_set():
    choices = Source.choices()
    valid_set = {
        "Endpoint",
        "GoogleDrive",
        "OneDrive",
        "Box",
        "Gmail",
        "Office365",
    }
    assert set(choices) == valid_set


def test_event_timestamp_gives_correct_json_representation():
    _filter = EventTimestamp.within_the_last(EventTimestamp.ONE_HOUR)
    expected = WITHIN_THE_LAST.format("eventTimestamp", "PT1H")
    assert str(_filter) == expected


@pytest.mark.parametrize(
    "key, value",
    [
        (EventTimestamp.FIFTEEN_MINUTES, u"PT15M"),
        (EventTimestamp.ONE_HOUR, u"PT1H"),
        (EventTimestamp.THREE_HOURS, u"PT3H"),
        (EventTimestamp.TWELVE_HOURS, u"PT12H"),
        (EventTimestamp.ONE_DAY, u"P1D"),
        (EventTimestamp.THREE_DAYS, u"P3D"),
        (EventTimestamp.SEVEN_DAYS, u"P7D"),
        (EventTimestamp.FOURTEEN_DAYS, u"P14D"),
        (EventTimestamp.THIRTY_DAYS, u"P30D"),
    ],
)
def test_all_event_timestamp_gives_correct_json_representation(key, value):

    _filter = EventTimestamp.within_the_last(key)
    expected = WITHIN_THE_LAST.format("eventTimestamp", value)
    assert str(_filter) == expected


def test_risk_indicator_mime_type_is_true_str_gives_correct_json_representation():
    _filter = MimeTypeMismatch.is_true()
    expected = IS.format("mimeTypeMismatch", "TRUE")
    assert str(_filter) == expected


def test_risk_indicator_mime_type_is_false_str_gives_correct_json_representation():
    _filter = MimeTypeMismatch.is_false()
    expected = IS.format("mimeTypeMismatch", "FALSE")
    assert str(_filter) == expected


def test_risk_indicator_active_hours_is_true_str_gives_correct_json_representation():
    _filter = OutsideActiveHours.is_true()
    expected = IS.format("outsideActiveHours", "TRUE")
    assert str(_filter) == expected


def test_risk_indicator_active_hours_is_false_str_gives_correct_json_representation():
    _filter = OutsideActiveHours.is_false()
    expected = IS.format("outsideActiveHours", "FALSE")
    assert str(_filter) == expected
