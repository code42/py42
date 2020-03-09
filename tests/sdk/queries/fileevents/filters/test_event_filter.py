from datetime import datetime
from time import time

from py42.sdk.queries.fileevents.filters.event_filter import (
    EventTimestamp,
    EventType,
    InsertionTimestamp,
    Source,
)
from tests.sdk.queries.conftest import (
    EXISTS,
    IN_RANGE,
    IS,
    IS_IN,
    IS_NOT,
    NOT_EXISTS,
    NOT_IN,
    ON_OR_AFTER,
    ON_OR_BEFORE,
    format_datetime,
    format_timestamp,
)


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
    _filter = EventType.eq("test_eventType")
    expected = IS.format("eventType", "test_eventType")
    assert str(_filter) == expected


def test_event_type_not_eq_str_gives_correct_json_representation():
    _filter = EventType.not_eq("test_eventType")
    expected = IS_NOT.format("eventType", "test_eventType")
    assert str(_filter) == expected


def test_event_type_is_in_str_gives_correct_json_representation():
    items = ["eventType1", "eventType2", "eventType3"]
    _filter = EventType.is_in(items)
    expected = IS_IN.format("eventType", *items)
    assert str(_filter) == expected


def test_event_type_not_in_str_gives_correct_json_representation():
    items = ["eventType1", "eventType2", "eventType3"]
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
    _filter = Source.eq("test_source")
    expected = IS.format("source", "test_source")
    assert str(_filter) == expected


def test_source_not_eq_str_gives_correct_json_representation():
    _filter = Source.not_eq("test_source")
    expected = IS_NOT.format("source", "test_source")
    assert str(_filter) == expected


def test_source_is_in_str_gives_correct_json_representation():
    items = ["source1", "source2", "source3"]
    _filter = Source.is_in(items)
    expected = IS_IN.format("source", *items)
    assert str(_filter) == expected


def test_source_not_in_str_gives_correct_json_representation():
    items = ["source1", "source2", "source3"]
    _filter = Source.not_in(items)
    expected = NOT_IN.format("source", *items)
    assert str(_filter) == expected
