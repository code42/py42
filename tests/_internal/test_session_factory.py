import pytest
from requests import Session

import py42
from py42._internal.async_session import Py42AsyncSession
from py42._internal.auth_handling import AuthHandler, CompositeModifier
from py42._internal.login_providers import FileEventLoginProvider
from py42._internal.session import Py42Session
from py42._internal.session_factory import AuthHandlerFactory, SessionFactory, SessionModifierFactory

TARGET_HOST_ADDRESS = "http://target"


class TestSessionFactory(object):

    @pytest.fixture
    def file_event_login_provider(self, mocker):
        return mocker.MagicMock(spec=FileEventLoginProvider)

    @pytest.fixture
    def session_modifier_factory(self, mocker):
        return mocker.MagicMock(spec=SessionModifierFactory)

    @pytest.fixture
    def auth_handler_factory(self, mocker):
        return mocker.MagicMock(spec=AuthHandlerFactory)

    def test_create_file_event_session_creates_session_with_address_from_provider(self,  session_modifier_factory,
                                                                                  auth_handler_factory,
                                                                                  file_event_login_provider):
        file_event_login_provider.get_target_host_address.return_value = TARGET_HOST_ADDRESS
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        session = factory.create_file_event_session(file_event_login_provider)
        assert session.host_address == TARGET_HOST_ADDRESS

    def test_create_file_event_session_calls_session_constructor_with_correct_args(self, mocker,
                                                                                   session_modifier_factory,
                                                                                   auth_handler_factory,
                                                                                   file_event_login_provider):
        file_event_login_provider.get_target_host_address.return_value = TARGET_HOST_ADDRESS
        auth_handler = mocker.MagicMock(spec=AuthHandler)
        auth_handler_factory.create_auth_handler.return_value = auth_handler
        mocker.patch('py42._internal.session_factory.call_session_constructor')

        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_file_event_session(file_event_login_provider)

        py42._internal.session_factory.call_session_constructor.assert_called_with(Py42Session, Session,
                                                                                   TARGET_HOST_ADDRESS, auth_handler)

    def test_create_file_event_session_uses_auth_handler_with_provider_and_modifier(self, mocker,
                                                                                    session_modifier_factory,
                                                                                    auth_handler_factory,
                                                                                    file_event_login_provider):
        modifier = mocker.MagicMock(spec=CompositeModifier)
        session_modifier_factory.create_v3_session_modifier.return_value = modifier
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory)
        factory.create_file_event_session(file_event_login_provider)
        auth_handler_factory.create_auth_handler.assert_called_with(file_event_login_provider, modifier)

    def test_create_file_event_session_with_is_async_true_creates_async_session(self, mocker, session_modifier_factory,
                                                                                auth_handler_factory,
                                                                                file_event_login_provider):
        mocker.patch('py42._internal.session_factory.call_session_constructor')
        factory = SessionFactory(Session, session_modifier_factory, auth_handler_factory, is_async=True)
        factory.create_file_event_session(file_event_login_provider)
        py42._internal.session_factory.call_session_constructor.assert_called_with(Py42AsyncSession, mocker.ANY,
                                                                                   mocker.ANY, mocker.ANY)
