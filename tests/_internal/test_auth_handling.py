from py42._internal.auth_handling import HeaderModifier, CookieModifier
from tests.shared_test_utils import MockRequestsSession

ORIGINAL_VALUE = "test-original-value"
UPDATED_VALUE = "test-updated-value"
CUSTOM_NAME = "Custom-Name"
DEFAULT_HEADER = "Authorization"


def test_header_modifier_constructs_successfully():
    assert HeaderModifier()


def test_header_modifier_adds_default_header_by_default():
    header_modifier = HeaderModifier()
    mock_session = MockRequestsSession()
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    assert DEFAULT_HEADER in mock_session.headers


def test_header_modifier_adds_specified_header():
    header_modifier = HeaderModifier(CUSTOM_NAME)
    mock_session = MockRequestsSession()
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    assert CUSTOM_NAME in mock_session.headers


def test_header_modifier_sets_default_header_to_given_value():
    header_modifier = HeaderModifier()
    mock_session = MockRequestsSession()
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    assert mock_session.headers.get(DEFAULT_HEADER) == ORIGINAL_VALUE


def test_header_modifier_sets_specified_header_to_given_value():
    header_modifier = HeaderModifier(CUSTOM_NAME)
    mock_session = MockRequestsSession()
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    assert mock_session.headers.get(CUSTOM_NAME) == ORIGINAL_VALUE


def test_header_modifier_updates_default_header_if_present():
    header_modifier = HeaderModifier()
    mock_session = MockRequestsSession()
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    header_modifier.modify_session(mock_session, UPDATED_VALUE)
    assert mock_session.headers.get(DEFAULT_HEADER) == UPDATED_VALUE


def test_header_modifier_updates_specified_header_if_present():
    header_modifier = HeaderModifier(CUSTOM_NAME)
    mock_session = MockRequestsSession()
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    header_modifier.modify_session(mock_session, UPDATED_VALUE)
    assert mock_session.headers.get(CUSTOM_NAME) == UPDATED_VALUE


def test_cookie_modifier_constructs_successfully():
    assert CookieModifier(CUSTOM_NAME)


def test_cookie_modifier_adds_specified_cookie():
    cookie_modifier = CookieModifier(CUSTOM_NAME)
    mock_session = MockRequestsSession()
    cookie_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    assert CUSTOM_NAME in mock_session.cookies
