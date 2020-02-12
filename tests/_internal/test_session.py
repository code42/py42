from json import dumps

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

    def test_session_request_calls_requests_with_timeout_param(self, success_requests_session):
        session = Py42Session(success_requests_session, HOST_ADDRESS)
        session.request("GET", URL)

        assert success_requests_session.request.call_args[1]["timeout"] == 60

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
        valid_auth_handler.renew_authentication.assert_called_once_with(session, use_cache=True)

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
            assert e.request.url == URL
