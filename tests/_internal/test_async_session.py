import py42.settings
from conftest import *

from py42._internal.async_session import Py42AsyncSession


class TestPy42AsyncSession(object):

    def test_request_without_catch_upon_exception_does_not_raise_exception(
            self, error_requests_session, renewing_auth_handler):

        session = Py42AsyncSession(error_requests_session, HOST_ADDRESS, renewing_auth_handler)
        session.get(URL, force_sync=True)
        assert True

    def test_request_without_catch_upon_exception_calls_global_receiver_with_message_and_trace(
            self, error_requests_session, renewing_auth_handler, http_error, catch, global_exception_message_receiver,
            traceback):

        session = Py42AsyncSession(error_requests_session, HOST_ADDRESS, renewing_auth_handler)
        session.get(URL, force_sync=True)
        message = build_expected_exception_message_with_trace(HOST_ADDRESS, URL, HTTPError, REQUEST_EXCEPTION_MESSAGE,
                                                              TRACEBACK)
        global_exception_message_receiver.assert_called_with(message)

    def test_request_with_catch_upon_exception_calls_catch_with_exception_message(
            self, error_requests_session, renewing_auth_handler, http_error, catch):

        session = Py42AsyncSession(error_requests_session, HOST_ADDRESS, renewing_auth_handler)
        session.get(URL, catch=catch, force_sync=True)
        exception = catch.call_args[0][0]  # first and only arg from list of ordered args
        assert type(exception) == HTTPError
        assert str(exception) == build_expected_exception_message(HOST_ADDRESS, URL, HTTPError,
                                                                  REQUEST_EXCEPTION_MESSAGE)

    def test_request_with_catch_upon_exception_does_not_call_global_receiver(
            self, error_requests_session, renewing_auth_handler, http_error, catch, global_exception_message_receiver):

        py42.settings.global_exception_message_receiver = global_exception_message_receiver
        session = Py42AsyncSession(error_requests_session, HOST_ADDRESS, renewing_auth_handler)
        session.get(URL, catch=catch, force_sync=True)
        global_exception_message_receiver.assert_not_called()

    def test_request_with_catch_upon_exception_calls_catch_with_exception_of_same_type_raised_internally(
            self, error_response, error_requests_session, renewing_auth_handler, http_error, catch):

        error_response.raise_for_status.side_effect = ZeroDivisionError()
        error_requests_session.request.return_value = error_response

        session = Py42AsyncSession(error_requests_session, HOST_ADDRESS, renewing_auth_handler)
        session.get(URL, catch=catch, force_sync=True)

        exception = catch.call_args[0][0]  # first and only arg from list of ordered args
        assert type(exception) == ZeroDivisionError
