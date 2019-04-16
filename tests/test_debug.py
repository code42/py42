import pytest
import py42.debug as debug
import py42.settings as settings
import py42.debug_level as debug_level


@pytest.fixture
def none_enabled():
    settings.debug_level = debug_level.NONE


@pytest.fixture
def info_enabled():
    settings.debug_level = debug_level.INFO


@pytest.fixture
def debug_enabled():
    settings.debug_level = debug_level.DEBUG


@pytest.fixture
def trace_enabled():
    settings.debug_level = debug_level.TRACE


@pytest.mark.parametrize("level", [debug_level.NONE], ids=["NONE"])
def test_will_print_for_given_none_enabled_with_none_returns_true(none_enabled, level):
    assert debug.will_print_for(level)


@pytest.mark.parametrize("level", [debug_level.INFO, debug_level.DEBUG, debug_level.TRACE], ids=["INFO", "DEBUG", "TRACE"])
def test_will_print_for_given_none_enabled_with_level_higher_than_none_returns_false(none_enabled, level):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize("level", [debug_level.NONE, debug_level.INFO], ids=["NONE", "INFO"])
def test_will_print_for_given_info_enabled_with_level_lower_than_or_equal_to_info_returns_true(info_enabled, level):
    assert debug.will_print_for(level)


@pytest.mark.parametrize("level", [debug_level.DEBUG, debug_level.TRACE], ids=["DEBUG", "TRACE"])
def test_will_print_for_given_info_enabled_with_level_higher_than_info_returns_false(info_enabled, level):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize("level", [debug_level.NONE, debug_level.INFO, debug_level.DEBUG], ids=["NONE", "INFO", "DEBUG"])
def test_will_print_for_given_debug_enabled_with_level_lower_than_or_equal_to_debug_returns_true(debug_enabled, level):
    assert debug.will_print_for(level)


@pytest.mark.parametrize("level", [debug_level.TRACE], ids=["TRACE"])
def test_will_print_for_given_debug_enabled_with_level_higher_than_debug_returns_false(debug_enabled, level):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize("level", [debug_level.NONE, debug_level.INFO, debug_level.DEBUG, debug_level.TRACE],
                         ids=["NONE", "INFO", "DEBUG", "TRACE"])
def test_will_print_for_given_trace_enabled_with_level_lower_than_or_equal_to_trace_returns_true(trace_enabled, level):
    assert debug.will_print_for(level)


@pytest.mark.parametrize("level", [-1, 4, 10])
def test_will_print_for_given_none_level_enabled_with_undefined_level_returns_false(none_enabled, level):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize("level", [-1, 4, 10])
def test_will_print_for_given_info_level_enabled_with_undefined_level_returns_false(info_enabled, level):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize("level", [-1, 4, 10])
def test_will_print_for_given_debug_level_enabled_with_undefined_level_returns_false(debug_enabled, level):
    assert not debug.will_print_for(level)


@pytest.mark.parametrize("level", [-1, 4, 10])
def test_will_print_for_given_trace_level_enabled_with_undefined_level_returns_false(trace_enabled, level):
    assert not debug.will_print_for(level)
