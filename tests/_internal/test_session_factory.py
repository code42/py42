import pytest
from requests import Session

from py42._internal.auth_handling import HeaderModifier
from py42._internal.session_factory import (
    AuthHandlerFactory,
    SessionFactory,
    SessionModifierFactory,
)
from py42._internal.token_providers import (
    BasicAuthProvider,
    C42APILoginTokenProvider,
    C42ApiV1TokenProvider,
    C42ApiV3TokenProvider,
)

TARGET_HOST_ADDRESS = "http://target-host-address.com"


class TestSessionFactory(object):
    @pytest.fixture
    def login_token_provider(self, mocker):
        provider = mocker.MagicMock(spec=C42APILoginTokenProvider)
        return provider

    @pytest.fixture
    def session_modifier_factory(self, mocker):
        return mocker.MagicMock(spec=SessionModifierFactory)

    @pytest.fixture
    def auth_handler_factory(self, mocker):
        return mocker.MagicMock(spec=AuthHandlerFactory)

    def test_create_basic_auth_session_creates_session_with_expected_address(
        self, session_modifier_factory, auth_handler_factory
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_basic_auth_session(TARGET_HOST_ADDRESS, u"username", u"password")
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_basic_auth_session_uses_auth_handler_with_expected_provider_and_modifier(
        self, mocker, session_modifier_factory, auth_handler_factory
    ):
        modifier = mocker.MagicMock(spec=HeaderModifier)
        session_modifier_factory.create_header_modifier.return_value = modifier
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_basic_auth_session(TARGET_HOST_ADDRESS, u"username", u"password")
        provider = auth_handler_factory.create_auth_handler.call_args[0][0]
        called_modifier = auth_handler_factory.create_auth_handler.call_args[0][1]
        assert type(provider) == BasicAuthProvider
        assert modifier == called_modifier

    def test_create_v1_session_creates_session_with_expected_address(
        self, session_modifier_factory, auth_handler_factory, mock_session
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_v1_session(TARGET_HOST_ADDRESS, mock_session)
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_v1_session_uses_auth_handler_with_expected_provider_and_modifier(
        self, mocker, session_modifier_factory, auth_handler_factory, mock_session
    ):
        modifier = mocker.MagicMock(spec=HeaderModifier)
        session_modifier_factory.create_header_modifier.return_value = modifier
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_v1_session(TARGET_HOST_ADDRESS, mock_session)
        provider = auth_handler_factory.create_auth_handler.call_args[0][0]
        called_modifier = auth_handler_factory.create_auth_handler.call_args[0][1]
        assert type(provider) == C42ApiV1TokenProvider
        assert modifier == called_modifier

    def test_create_jwt_session_creates_session_with_expected_address(
        self, session_modifier_factory, auth_handler_factory, mock_session
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_jwt_session(TARGET_HOST_ADDRESS, mock_session)
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_jwt_session_uses_auth_handler_with_expected_provider_and_modifier(
        self, mocker, session_modifier_factory, auth_handler_factory, mock_session
    ):
        modifier = mocker.MagicMock(spec=HeaderModifier)
        session_modifier_factory.create_header_modifier.return_value = modifier
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_jwt_session(TARGET_HOST_ADDRESS, mock_session)
        provider = auth_handler_factory.create_auth_handler.call_args[0][0]
        called_modifier = auth_handler_factory.create_auth_handler.call_args[0][1]
        assert type(provider) == C42ApiV3TokenProvider
        assert modifier == called_modifier

    def test_create_storage_session_creates_session_with_expected_address(
        self, session_modifier_factory, auth_handler_factory, login_token_provider
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_storage_session(TARGET_HOST_ADDRESS, login_token_provider)
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_storage_session_uses_auth_handler_with_expected_provider_and_modifier(
        self, mocker, session_modifier_factory, auth_handler_factory, login_token_provider
    ):
        modifier = mocker.MagicMock(spec=HeaderModifier)
        session_modifier_factory.create_header_modifier.return_value = modifier
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_storage_session(TARGET_HOST_ADDRESS, login_token_provider)
        provider = auth_handler_factory.create_auth_handler.call_args[0][0]
        called_modifier = auth_handler_factory.create_auth_handler.call_args[0][1]
        assert type(provider) == C42ApiV1TokenProvider
        assert modifier == called_modifier

    def test_create_anonymous_session_creates_session_with_expected_address(
        self, session_modifier_factory, auth_handler_factory
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_anonymous_session(TARGET_HOST_ADDRESS)
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_anonymous_session_does_not_use_auth_handler(
        self, session_modifier_factory, auth_handler_factory
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_anonymous_session(TARGET_HOST_ADDRESS)
        assert auth_handler_factory.create_auth_handler.call_count == 0
