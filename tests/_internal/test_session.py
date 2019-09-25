from json import dumps

import py42.settings
from py42._internal.compat import str
from py42._internal.session import Py42Session
from .conftest import *


class TestPy42Session(object):
    def test_session_post_with_json_calls_filter_out_none_util(
        self, mocker, success_requests_session
    ):
        session = Py42Session(success_requests_session, HOST_ADDRESS)
        filter_out_none_mock = mocker.patch("py42.util.filter_out_none")
        filter_out_none_mock.return_value = {}

        session.post(URL, json=JSON_VALUE)

        assert filter_out_none_mock.call_count == 1

    def test_session_post_with_json_calls_request_with_data_param_with_string_encoded_json(
        self, success_requests_session
    ):
        session = Py42Session(success_requests_session, HOST_ADDRESS)
        session.post(URL, json=JSON_VALUE)
        assert success_requests_session.request.call_args[KWARGS_INDEX][DATA_KEY] == dumps(
            JSON_VALUE
        )

    def test_session_post_with_data_and_json_params_overwrites_data_with_json(
        self, success_requests_session
    ):
        session = Py42Session(success_requests_session, HOST_ADDRESS)
        session.post(URL, data=DATA_VALUE, json=JSON_VALUE)
        assert success_requests_session.request.call_args[KWARGS_INDEX][DATA_KEY] == dumps(
            JSON_VALUE
        )

    def test_session_post_with_data_and_json_params_does_not_pass_json_param_to_request(
        self, success_requests_session
    ):
        session = Py42Session(success_requests_session, HOST_ADDRESS)
        session.post(URL, data=DATA_VALUE, json=JSON_VALUE)
        assert success_requests_session.request.call_args[KWARGS_INDEX].get(JSON_KEY) is None

    def test_session_request_returns_response_when_good_status_code(self, success_requests_session):
        session = Py42Session(success_requests_session, HOST_ADDRESS)
        response = session.get(URL)
        assert response.text == TEST_RESPONSE_CONTENT

    def test_session_request_with_error_status_code_raises_http_error(self, error_requests_session):
        session = Py42Session(error_requests_session, HOST_ADDRESS)
        with pytest.raises(HTTPError):
            session.get(URL)

    def test_session_request_calls_auth_handler_renew_authentication_with_correct_params_when_making_first_request(
        self, success_requests_session, valid_auth_handler
    ):
        session = Py42Session(success_requests_session, HOST_ADDRESS, valid_auth_handler)
        session.get(URL)
        valid_auth_handler.renew_authentication.assert_called_once_with(
            session, use_credential_cache=True
        )

    def test_session_request_calls_auth_handler_renew_authentication_only_once_while_auth_is_valid(
        self, success_requests_session, valid_auth_handler
    ):
        session = Py42Session(success_requests_session, HOST_ADDRESS, valid_auth_handler)
        session.get(URL)
        session.get(URL)
        assert valid_auth_handler.renew_authentication.call_count == 1

    def test_session_request_calls_auth_handler_renew_authentication_twice_when_response_unauthorized(
        self, success_requests_session, renewing_auth_handler
    ):
        session = Py42Session(success_requests_session, HOST_ADDRESS, renewing_auth_handler)
        session.get(URL)  # initialize
        assert success_requests_session.request.call_count == 1
        session.get(URL)  # second request will be unauthorized and call renew_authentication again
        assert renewing_auth_handler.renew_authentication.call_count == 2

    def test_session_request_called_again_twice_when_response_unauthorized(
        self, success_requests_session, renewing_auth_handler
    ):
        session = Py42Session(success_requests_session, HOST_ADDRESS, renewing_auth_handler)
        session.get(URL)  # initialize
        assert success_requests_session.request.call_count == 1
        session.get(URL)  # second request will be unauthorized and call request again
        assert success_requests_session.request.call_count == 3

    def test_request_upon_exception_url_included_in_message(
        self, error_requests_session, renewing_auth_handler
    ):
        session = Py42Session(error_requests_session, HOST_ADDRESS, renewing_auth_handler)
        with pytest.raises(HTTPError) as e:
            session.get(URL)
        expected = build_expected_exception_message(
            HOST_ADDRESS, URL, HTTPError, REQUEST_EXCEPTION_MESSAGE
        )
        assert e.value.args[0] == expected

    def test_request_with_catch_upon_exception_calls_catch_with_exception_message(
        self, error_requests_session, renewing_auth_handler, http_error, catch
    ):

        session = Py42Session(error_requests_session, HOST_ADDRESS, renewing_auth_handler)
        session.get(URL, catch=catch)
        exception = catch.call_args[0][0]  # first and only arg from list of ordered args
        assert type(exception) == HTTPError
        assert str(exception) == build_expected_exception_message(
            HOST_ADDRESS, URL, HTTPError, REQUEST_EXCEPTION_MESSAGE
        )

    def test_request_with_catch_upon_exception_does_not_call_global_receiver(
        self,
        error_requests_session,
        renewing_auth_handler,
        http_error,
        catch,
        global_exception_message_receiver,
    ):

        py42.settings.global_exception_message_receiver = global_exception_message_receiver
        session = Py42Session(error_requests_session, HOST_ADDRESS, renewing_auth_handler)
        session.get(URL, catch=catch)
        global_exception_message_receiver.assert_not_called()

    def test_request_without_catch_upon_exception_calls_global_receiver_with_message_and_trace(
        self,
        error_requests_session,
        renewing_auth_handler,
        http_error,
        catch,
        global_exception_message_receiver,
        traceback,
    ):

        session = Py42Session(error_requests_session, HOST_ADDRESS, renewing_auth_handler)
        with pytest.raises(Exception):
            session.get(URL)
        message = build_expected_exception_message_with_trace(
            HOST_ADDRESS, URL, HTTPError, REQUEST_EXCEPTION_MESSAGE, TRACEBACK
        )
        global_exception_message_receiver.assert_called_once_with(message)

    def test_request_with_catch_upon_exception_calls_catch_with_exception_of_same_type_raised_internally(
        self, error_response, error_requests_session, renewing_auth_handler, http_error, catch
    ):

        error_response.raise_for_status.side_effect = ZeroDivisionError()
        error_requests_session.request.return_value = error_response

        session = Py42Session(error_requests_session, HOST_ADDRESS, renewing_auth_handler)
        session.get(URL, catch=catch)

        exception = catch.call_args[0][0]  # first and only arg from list of ordered args
        assert type(exception) == ZeroDivisionError
