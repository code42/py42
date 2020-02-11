import pytest
from requests import Session

from py42._internal.auth_handling import CompositeModifier, HeaderModifier
from py42._internal.login_providers import (
    BasicAuthProvider,
    C42ApiV1TokenProvider,
    FileEventLoginProvider,
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
        self, session_modifier_factory, auth_handler_factory, success_requests_session
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_basic_auth_session(TARGET_HOST_ADDRESS, u"username", u"password")
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_file_event_session_creates_session_with_address_from_provider(
        self, session_modifier_factory, auth_handler_factory, file_event_login_provider
    ):
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_file_event_session(file_event_login_provider)
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_file_event_session_uses_auth_handler_with_expected_provider_and_modifier(
        self, mocker, session_modifier_factory, auth_handler_factory, file_event_login_provider
    ):
        modifier = mocker.MagicMock(spec=CompositeModifier)
        session_modifier_factory.create_v3_session_modifier.return_value = modifier
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_file_event_session(file_event_login_provider)
        auth_handler_factory.create_auth_handler.assert_called_once_with(
            file_event_login_provider, modifier
        )
