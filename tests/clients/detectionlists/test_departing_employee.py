# -*- coding: utf-8 -*-

import json

import pytest

from py42._internal.clients.detection_list_user import DetectionListUserClient
from py42.clients.detectionlists.departing_employee import DepartingEmployeeClient
from py42.clients.users import UserClient
from tests.conftest import TENANT_ID_FROM_RESPONSE

_TENANT_ID_PARAM = "22222222-2222-2222-2222-222222222222"
_USER_ID = "890973079883949999"

_GET_CASE_DETAILS_RESPONSE = """
{{
    "tenantId":"{0}",
    "caseId":"697",
    "userUid":"921286907298179098",
    "userName":"test.example@example.com",
    "displayName":"Test Testerson",
    "notes":"notes notes notes",
    "createdAt":"2020-02-14T20:11:29.5563480Z",
    "status":"OPEN",
    "cloudUsernames":["test.testerson+partners@example.com","test.s@example.com"],
    "departureDate":"2020-02-13",
    "alertsEnabled":true
}}
""".format(
    TENANT_ID_FROM_RESPONSE
)


_GET_ALL_CASES_RESPONSE = """
{{
"items": [
 {{"type$": "DEPARTING_EMPLOYEE_V2",
 "tenantId": {0},
 "userId": "890973079883949999",
 "userName": "test@example.com",
 "displayName": "Name",
 "notes": "",
 "createdAt": "2019-10-25T13:31:14.1199010Z",
 "status": "OPEN",
 "cloudUsernames": ["test@example.com"],
 "totalBytes": 139856482,
 "numEvents": 11
}}],
"totalCount": 1
}}
""".format(
    _TENANT_ID_PARAM
)

_GET_ALL_CASES_EMPTY_RESPONSE = """
{"type$":"DEPARTING_EMPLOYEE_SEARCH_RESPONSE","cases":[],"totalCount":0}
"""


class TestDepartingEmployeeClient(object):
    @pytest.fixture
    def mock_get_all_cases_response(self, mocker, py42_response):
        py42_response.text = _GET_ALL_CASES_RESPONSE

        return py42_response

    @pytest.fixture
    def mock_get_all_cases_response_empty(self, mocker, py42_response):
        py42_response.text = _GET_ALL_CASES_EMPTY_RESPONSE
        return py42_response

    @pytest.fixture
    def mock_user_client(self, mock_session, user_context, py42_response):
        user_client = UserClient(mock_session)
        mock_session.post.return_value = py42_response
        return user_client

    @pytest.fixture
    def mock_detection_list_user_client(
        self, mock_session, user_context, py42_response, mock_user_client
    ):
        user_client = DetectionListUserClient(mock_session, user_context, mock_user_client)
        mock_session.post.return_value = py42_response
        return user_client

    @pytest.fixture
    def mock_py42_response(self, mocker, mock_get_case_details_function, py42_response):
        py42_response.test = mock_get_case_details_function.text

        return py42_response

    def test_add_posts_expected_data_and_to_expected_url(
        self,
        mock_session,
        user_context,
        mock_get_all_cases_response,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        user_context.get_current_tenant_id.return_value = _TENANT_ID_PARAM
        # Return value should have been set based on the arguments passed
        # in add, here however as we are mocking it, it doesn't matter. Can be refactored
        mock_session.post.return_value = mock_get_all_cases_response
        client.add(_USER_ID, "2022-12-20")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["userId"] == _USER_ID
            and posted_data["tenantId"] == _TENANT_ID_PARAM
            and posted_data["departureDate"] == "2022-12-20"
        )
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/departingemployee/add"
        assert mock_session.post.call_count == 2

    def test_remove_posts_expected_data_and_to_expected_url(
        self,
        mock_session,
        user_context,
        mock_get_all_cases_response_empty,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.remove("999")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert posted_data["userId"] == "999" and posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/departingemployee/remove"

    def test_get_all_posts_expected_data_to_expected_url(
        self,
        mock_session,
        user_context,
        mock_get_all_cases_response,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        mock_session.post.return_value = mock_get_all_cases_response
        for _ in client.get_all():
            break
        first_call = mock_session.post.call_args_list[0]
        posted_data = json.loads(first_call[1]["data"])
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["pgSize"] == 100
            and posted_data["pgNum"] == 1
            and posted_data["filterType"] == "OPEN"
            and posted_data["srtKey"] == "CREATED_AT"
            and posted_data["srtDirection"] == "DESC"
        )
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/departingemployee/search"
        assert mock_session.post.call_count == 1

    def test_get_departing_employee_page_posts_data_to_expected_url(
        self,
        mock_session,
        user_context,
        mock_get_all_cases_response,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        client.get_departing_employees_page(
            filter_type="OPEN",
            sort_key="CREATED_AT",
            sort_direction="DESC",
            page_num=1,
            page_size=100,
        )
        mock_session.post.return_value = mock_get_all_cases_response
        first_call = mock_session.post.call_args_list[0]
        posted_data = json.loads(first_call[1]["data"])
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["pgSize"] == 100
            and posted_data["pgNum"] == 1
            and posted_data["filterType"] == "OPEN"
            and posted_data["srtKey"] == "CREATED_AT"
            and posted_data["srtDirection"] == "DESC"
        )
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/departingemployee/search"
        assert mock_session.post.call_count == 1

    def test_set_alerts_enabled_posts_expected_data(
        self,
        mock_session,
        user_context,
        mock_get_all_cases_response_empty,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.set_alerts_enabled()

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["alertsEnabled"] is True
        )

    def test_set_alerts_enabled_posts_to_expected_url(
        self,
        mock_session,
        user_context,
        mock_get_all_cases_response_empty,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.set_alerts_enabled()
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/departingemployee/setalertstate"

    def test_get_posts_expected_data(
        self,
        mock_session,
        user_context,
        mock_get_all_cases_response_empty,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.get("999")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE and posted_data["userId"] == "999"

    def test_get_posts_to_expected_url(
        self,
        mock_session,
        user_context,
        mock_get_all_cases_response_empty,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        mock_session.post.return_value = mock_get_all_cases_response_empty
        client.get("999")
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/departingemployee/get"

    def test_update_posts_expected_data(
        self,
        mock_session,
        user_context,
        mock_get_all_cases_response,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        mock_session.post.return_value = mock_get_all_cases_response
        client.update_departure_date(_USER_ID, "2020-12-20")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert (
            posted_data["userId"] == _USER_ID
            and posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["departureDate"] == "2020-12-20"
        )

    def test_update_posts_to_expected_url(
        self, mock_session, user_context, mock_detection_list_user_client
    ):
        client = DepartingEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        client.update_departure_date(_USER_ID, "2022-12-20")
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/departingemployee/update"
