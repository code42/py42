import pytest
import logging

import py42
from py42.settings import debug


@pytest.fixture
def none_enabled():
    py42.settings.debug.level = debug.NONE


@pytest.fixture
def warning_enabled():
    py42.settings.debug.level = logging.WARNING
    yield warning_enabled
    py42.settings.debug.level = debug.NONE


@pytest.fixture
def info_enabled():
    py42.settings.debug.level = debug.INFO
    yield info_enabled
    py42.settings.debug.level = debug.NONE


@pytest.fixture
def debug_enabled():
    py42.settings.debug.level = debug.DEBUG
    yield debug_enabled
    py42.settings.debug.level = debug.NONE


@pytest.fixture
def trace_enabled():
    py42.settings.debug.level = debug.TRACE
    yield trace_enabled
    py42.settings.debug.level = debug.NONE


test_logger_name = "test"


@pytest.fixture
def custom_logger():
    default_logger = py42.settings.debug.logger
    py42.settings.debug.logger = logging.getLogger(test_logger_name)
    yield custom_logger
    py42.settings.debug.logger = default_logger


def test_setting_debug_level_to_warning_sets_default_logger_to_warning(warning_enabled):
    assert debug.logger.level == logging.WARNING


def test_setting_debug_level_to_info_sets_default_logger_to_info(info_enabled):
    assert debug.logger.level == logging.INFO


def test_setting_debug_level_to_debug_sets_default_logger_to_debug(debug_enabled):
    assert debug.logger.level == logging.DEBUG


def test_setting_debug_level_to_trace_sets_default_logger_to_debug(debug_enabled):
    assert debug.logger.level == logging.DEBUG


def test_setting_debug_level_to_warning_sets_custom_logger_to_warning(
    custom_logger, warning_enabled
):
    assert debug.logger.name == test_logger_name
    assert debug.logger.level == logging.WARNING


def test_setting_debug_level_to_info_sets_custom_logger_to_info(custom_logger, info_enabled):
    assert debug.logger.name == test_logger_name
    assert debug.logger.level == logging.INFO


def test_setting_debug_level_to_debug_sets_custom_logger_to_debug(custom_logger, debug_enabled):
    assert debug.logger.name == test_logger_name
    assert debug.logger.level == logging.DEBUG


def test_setting_debug_level_to_trace_sets_custom_logger_to_debug(custom_logger, debug_enabled):
    assert debug.logger.name == test_logger_name
    assert debug.logger.level == logging.DEBUG


def test_debug_settings_class_creates_default_logger():
    assert debug.logger.name == "py42"
    assert debug.level == logging.NOTSET
