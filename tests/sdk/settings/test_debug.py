import pytest

import py42
import py42.sdk.settings.debug as debug


@pytest.fixture
def none_enabled():
    py42.sdk.settings.debug.level = debug.NONE


@pytest.fixture
def info_enabled():
    py42.sdk.settings.debug.level = debug.INFO
    yield info_enabled
    py42.sdk.settings.debug.level = debug.NONE


@pytest.fixture
def debug_enabled():
    py42.sdk.settings.debug.level = debug.DEBUG
    yield debug_enabled
    py42.sdk.settings.debug.level = debug.NONE


@pytest.fixture
def trace_enabled():
    py42.sdk.settings.debug.level = debug.TRACE
    yield trace_enabled
    py42.sdk.settings.debug.level = debug.NONE


@pytest.mark.parametrize("level", [debug.NONE], ids=["NONE"])
def test_will_print_for_given_none_enabled_with_none_returns_true(none_enabled, level):
    assert debug.will_print_for(level)


@pytest.mark.parametrize(
    "level", [debug.INFO, debug.DEBUG, debug.TRACE], ids=["INFO", "DEBUG", "TRACE"]
)
def test_will_print_for_given_none_enabled_with_level_higher_than_none_returns_false(
    none_enabled, level
):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize("level", [debug.NONE, debug.INFO], ids=["NONE", "INFO"])
def test_will_print_for_given_info_enabled_with_level_lower_than_or_equal_to_info_returns_true(
    info_enabled, level
):
    assert debug.will_print_for(level)


@pytest.mark.parametrize("level", [debug.DEBUG, debug.TRACE], ids=["DEBUG", "TRACE"])
def test_will_print_for_given_info_enabled_with_level_higher_than_info_returns_false(
    info_enabled, level
):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize(
    "level", [debug.NONE, debug.INFO, debug.DEBUG], ids=["NONE", "INFO", "DEBUG"]
)
def test_will_print_for_given_debug_enabled_with_level_lower_than_or_equal_to_debug_returns_true(
    debug_enabled, level
):
    assert debug.will_print_for(level)


@pytest.mark.parametrize("level", [debug.TRACE], ids=["TRACE"])
def test_will_print_for_given_debug_enabled_with_level_higher_than_debug_returns_false(
    debug_enabled, level
):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize(
    "level",
    [debug.NONE, debug.INFO, debug.DEBUG, debug.TRACE],
    ids=["NONE", "INFO", "DEBUG", "TRACE"],
)
def test_will_print_for_given_trace_enabled_with_level_lower_than_or_equal_to_trace_returns_true(
    trace_enabled, level
):
    assert debug.will_print_for(level)


@pytest.mark.parametrize("level", [-1, 4, 10])
def test_will_print_for_given_none_level_enabled_with_undefined_level_returns_false(
    none_enabled, level
):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize("level", [-1, 4, 10])
def test_will_print_for_given_info_level_enabled_with_undefined_level_returns_false(
    info_enabled, level
):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize("level", [-1, 4, 10])
def test_will_print_for_given_debug_enabled_with_undefined_level_returns_false(
    debug_enabled, level
):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize("level", [-1, 4, 10])
def test_will_print_for_given_trace_level_enabled_with_undefined_level_returns_false(
    trace_enabled, level
):
    assert not debug.will_print_for(level)
