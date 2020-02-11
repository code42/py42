import pytest
from requests import Response

from py42._internal.auth_handling import (
    AuthHandler,
    CookieModifier,
    HeaderModifier,
    LoginProvider,
    SessionModifier,
)
from py42._internal.session import Py42Session

ORIGINAL_VALUE = "test-original-value"
UPDATED_VALUE = "test-updated-value"
CUSTOM_NAME = "Custom-Name"
DEFAULT_HEADER = "Authorization"

TEST_SECRET = "TEST-SECRET"


@pytest.fixture
def mock_login_provider(mocker):
    provider = mocker.MagicMock(spec=LoginProvider)
    provider.get_secret_value.return_value = TEST_SECRET
    return provider


@pytest.fixture
def mock_session_modifier(mocker):
    return mocker.MagicMock(spec=SessionModifier)


def test_auth_handler_constructs_successfully():
    assert AuthHandler(LoginProvider(), SessionModifier())


def test_auth_handler_renew_authentication_using_cache_calls_get_secret_value_on_login_provider_with_correct_params(
    mock_login_provider, mock_session_modifier, mock_session
):
    auth_handler = AuthHandler(mock_login_provider, mock_session_modifier)
    auth_handler.renew_authentication(mock_session, use_cache=True)
    mock_login_provider.get_secret_value.assert_called_once_with(force_refresh=False)


def test_auth_handler_renew_authentication_no_cache_calls_get_secret_value_on_login_provider_with_correct_params(
    mock_login_provider, mock_session_modifier, mock_session
):
    auth_handler = AuthHandler(mock_login_provider, mock_session_modifier)
    auth_handler.renew_authentication(mock_session)
    mock_login_provider.get_secret_value.assert_called_once_with(force_refresh=True)


def test_auth_handler_renew_authentication_using_cache_calls_modify_session_on_session_modifier_with_correct_params(
    mock_login_provider, mock_session_modifier, mock_session
):
    auth_handler = AuthHandler(mock_login_provider, mock_session_modifier)
    auth_handler.renew_authentication(mock_session, use_cache=True)
    mock_session_modifier.modify_session.assert_called_once_with(mock_session, TEST_SECRET)


def test_auth_handler_renew_authentication_no_cache_calls_modify_session_on_session_modifier_with_correct_params(
    mock_login_provider, mock_session_modifier, mock_session
):
    auth_handler = AuthHandler(mock_login_provider, mock_session_modifier)
    auth_handler.renew_authentication(mock_session)
    mock_session_modifier.modify_session.assert_called_once_with(mock_session, TEST_SECRET)


def test_auth_handler_response_indicates_unauthorized_returns_true_for_401(mocker):
    mock_response = mocker.MagicMock(spec=Response)
    mock_response.status_code = 401
    assert AuthHandler.response_indicates_unauthorized(mock_response)


def test_auth_handler_response_indicates_unauthorized_returns_false_for_non_401(mocker):
    mock_response = mocker.MagicMock(spec=Response)
    mock_response.status_code = 200
    assert not AuthHandler.response_indicates_unauthorized(mock_response)


def test_header_modifier_constructs_successfully():
    assert HeaderModifier()


def test_header_modifier_adds_default_header_by_default(mock_session):
    header_modifier = HeaderModifier()
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    assert DEFAULT_HEADER in mock_session.headers


def test_header_modifier_adds_specified_header(mock_session):
    header_modifier = HeaderModifier(CUSTOM_NAME)
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    assert CUSTOM_NAME in mock_session.headers


def test_header_modifier_sets_default_header_to_given_value(mock_session):
    header_modifier = HeaderModifier()
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    assert mock_session.headers.get(DEFAULT_HEADER) == ORIGINAL_VALUE


def test_header_modifier_sets_specified_header_to_given_value(mock_session):
    header_modifier = HeaderModifier(CUSTOM_NAME)
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    assert mock_session.headers.get(CUSTOM_NAME) == ORIGINAL_VALUE


def test_header_modifier_updates_default_header_if_present(mock_session):
    header_modifier = HeaderModifier()
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    header_modifier.modify_session(mock_session, UPDATED_VALUE)
    assert mock_session.headers.get(DEFAULT_HEADER) == UPDATED_VALUE


def test_header_modifier_updates_specified_header_if_present(mock_session):
    header_modifier = HeaderModifier(CUSTOM_NAME)
    header_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    header_modifier.modify_session(mock_session, UPDATED_VALUE)
    assert mock_session.headers.get(CUSTOM_NAME) == UPDATED_VALUE


def test_cookie_modifier_constructs_successfully():
    assert CookieModifier(CUSTOM_NAME)


def test_cookie_modifier_adds_specified_cookie(mock_session):
    from .conftest import cookie_dict

    cookie_modifier = CookieModifier(CUSTOM_NAME)
    cookie_modifier.modify_session(mock_session, ORIGINAL_VALUE)
    assert mock_session.cookies.get(CUSTOM_NAME) is not None
    cookie_dict.clear()
