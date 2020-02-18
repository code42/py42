import pytest
from requests import Session

from py42._internal.auth_handling import CompositeModifier, HeaderModifier
from py42._internal.login_providers import (
    BasicAuthProvider,
    C42APILoginTokenProvider,
    C42ApiV1TokenProvider,
    C42ApiV3TokenProvider,
    FileEventLoginProvider,
    KeyValueStoreLoginProvider,
)
from py42._internal.session_factory import (
    AuthHandlerFactory,
    SessionFactory,
    SessionModifierFactory,
)

TARGET_HOST_ADDRESS = "http://target-host-address.com"


class TestSessionFactory(object):
    @pytest.fixture
    def file_event_login_provider(self, mocker):
        provider = mocker.MagicMock(spec=FileEventLoginProvider)
        provider.get_target_host_address.return_value = TARGET_HOST_ADDRESS
        return provider

    @pytest.fixture
    def key_value_store_login_provider(self, mocker):
        provider = mocker.MagicMock(spec=KeyValueStoreLoginProvider)
        provider.get_target_host_address.return_value = TARGET_HOST_ADDRESS
        return provider

    @pytest.fixture
    def login_token_provider(self, mocker):
        provider = mocker.MagicMock(spec=C42APILoginTokenProvider)
        provider.get_target_host_address.return_value = TARGET_HOST_ADDRESS
        return provider

    @pytest.fixture
    def session_modifier_factory(self, mocker):
        return mocker.MagicMock(spec=SessionModifierFactory)

    @pytest.fixture
    def auth_handler_factory(self, mocker):
        return mocker.MagicMock(spec=AuthHandlerFactory)

    def test_create_basic_auth_session_creates_session_with_address_from_provider(
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

    def test_create_v1_session_creates_session_with_address_from_provider(
        self, session_modifier_factory, auth_handler_factory, mock_session
    ):
        mock_session.host_address = TARGET_HOST_ADDRESS
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_v1_session(mock_session)
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_v1_session_uses_auth_handler_with_expected_provider_and_modifier(
        self, mocker, session_modifier_factory, auth_handler_factory, mock_session
    ):
        modifier = mocker.MagicMock(spec=HeaderModifier)
        mock_session.host_address = TARGET_HOST_ADDRESS
        session_modifier_factory.create_header_modifier.return_value = modifier
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_v1_session(mock_session)
        provider = auth_handler_factory.create_auth_handler.call_args[0][0]
        called_modifier = auth_handler_factory.create_auth_handler.call_args[0][1]
        assert type(provider) == C42ApiV1TokenProvider
        assert modifier == called_modifier

    def test_create_jwt_session_creates_session_with_address_from_provider(
        self, session_modifier_factory, auth_handler_factory, mock_session
    ):
        mock_session.host_address = TARGET_HOST_ADDRESS
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_jwt_session(mock_session)
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_jwt_session_uses_auth_handler_with_expected_provider_and_modifier(
        self, mocker, session_modifier_factory, auth_handler_factory, mock_session
    ):
        modifier = mocker.MagicMock(spec=CompositeModifier)
        mock_session.host_address = TARGET_HOST_ADDRESS
        session_modifier_factory.create_v3_session_modifier.return_value = modifier
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_jwt_session(mock_session)
        provider = auth_handler_factory.create_auth_handler.call_args[0][0]
        called_modifier = auth_handler_factory.create_auth_handler.call_args[0][1]
        assert type(provider) == C42ApiV3TokenProvider
        assert modifier == called_modifier

    def test_create_storage_session_creates_session_with_address_from_provider(
        self, session_modifier_factory, auth_handler_factory, login_token_provider
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_storage_session(login_token_provider)
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_storage_session_uses_auth_handler_with_expected_provider_and_modifier(
        self, mocker, session_modifier_factory, auth_handler_factory, login_token_provider
    ):
        modifier = mocker.MagicMock(spec=HeaderModifier)
        session_modifier_factory.create_header_modifier.return_value = modifier
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_storage_session(login_token_provider)
        provider = auth_handler_factory.create_auth_handler.call_args[0][0]
        called_modifier = auth_handler_factory.create_auth_handler.call_args[0][1]
        assert type(provider) == C42ApiV1TokenProvider
        assert modifier == called_modifier

    def test_create_key_value_store_session_creates_session_with_address_from_provider(
        self, session_modifier_factory, auth_handler_factory, key_value_store_login_provider
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_key_value_store_session(key_value_store_login_provider)
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_key_value_store_session_does_not_use_auth_handler(
        self, session_modifier_factory, auth_handler_factory, key_value_store_login_provider
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_key_value_store_session(key_value_store_login_provider)
        assert auth_handler_factory.create_auth_handler.call_count == 0

    def test_create_jwt_session_from_provider_creates_session_with_address_from_provider(
        self, session_modifier_factory, auth_handler_factory, file_event_login_provider
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_jwt_session_from_provider(file_event_login_provider)
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_jwt_session_from_provider_uses_auth_handler_with_provider_and_modifier(
        self, mocker, session_modifier_factory, auth_handler_factory, file_event_login_provider
    ):
        modifier = mocker.MagicMock(spec=CompositeModifier)
        session_modifier_factory.create_v3_session_modifier.return_value = modifier
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_jwt_session_from_provider(file_event_login_provider)
        auth_handler_factory.create_auth_handler.assert_called_once_with(
            file_event_login_provider, modifier
        )
