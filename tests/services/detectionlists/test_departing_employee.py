from datetime import datetime

import pytest
from tests.conftest import create_mock_error
from tests.conftest import create_mock_response
from tests.conftest import TENANT_ID_FROM_RESPONSE

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42UserAlreadyAddedError
from py42.exceptions import Py42UserNotOnListError
from py42.services.detectionlists.departing_employee import DepartingEmployeeFilters
from py42.services.detectionlists.departing_employee import DepartingEmployeeService
from py42.services.detectionlists.user_profile import DetectionListUserService
from py42.services.users import UserService

_TENANT_ID_PARAM = "22222222-2222-2222-2222-222222222222"
_USER_ID = "890973079883949999"


_GET_ALL_RESPONSE = """
{{
  "items": [
    {{
      "type$": "DEPARTING_EMPLOYEE_V2",
      "tenantId": "{0}",
      "userId": "890973079883949999",
      "userName": "test@example.com",
      "displayName": "Name",
      "notes": "",
      "createdAt": "2019-10-25T13:31:14.1199010Z",
      "status": "OPEN",
      "cloudUsernames": [
        "test@example.com"
      ],
      "totalBytes": 139856482,
      "numEvents": 11
    }}
  ],
  "totalCount": 1
}}
""".format(
    _TENANT_ID_PARAM
)

_GET_ALL_EMPTY_RESPONSE = """
{
    "type$":"DEPARTING_EMPLOYEE_SEARCH_RESPONSE",
    "items":[],
    "totalCount":0
}
"""


class TestDepartingEmployeeFilters:
    def test_choices_are_correct(self):
        actual = DepartingEmployeeFilters.choices()
        expected = [
            "OPEN",
            "LEAVING_TODAY",
            "EXFILTRATION_24_HOURS",
            "EXFILTRATION_30_DAYS",
        ]
        assert set(actual) == set(expected)


class TestDepartingEmployeeClient:
    @pytest.fixture
    def mock_get_all_response(self, mocker):
        yield create_mock_response(mocker, _GET_ALL_RESPONSE)

    @pytest.fixture
    def mock_get_all_response_empty(self, mocker):
        yield create_mock_response(mocker, _GET_ALL_EMPTY_RESPONSE)

    @pytest.fixture
    def mock_user_client(self, mock_connection, user_context, mocker):
        user_client = UserService(mock_connection)
        mock_connection.post.return_value = create_mock_response(mocker, "{}")
        return user_client

    @pytest.fixture
    def mock_detection_list_user_client(
        self, mock_connection, user_context, mocker, mock_user_client
    ):
        user_client = DetectionListUserService(
            mock_connection, user_context, mock_user_client
        )
        mock_connection.post.return_value = create_mock_response(mocker, "{}")
        return user_client

    @pytest.mark.parametrize(
        "departing_date",
        [("2022-12-20"), (datetime.strptime("2022-12-20", "%Y-%m-%d"))],
    )
    def test_add_posts_expected_data_and_to_expected_url(
        self,
        mock_connection,
        user_context,
        mock_get_all_response,
        mock_detection_list_user_client,
        departing_date,
    ):
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        user_context.get_current_tenant_id.return_value = _TENANT_ID_PARAM
        # Return value should have been set based on the arguments passed
        # in add, here however as we are mocking it, it doesn't matter. Can be refactored
        mock_connection.post.return_value = mock_get_all_response
        client.add(_USER_ID, departing_date)

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = mock_connection.post.call_args[1]["json"]
        assert (
            posted_data["userId"] == _USER_ID
            and posted_data["tenantId"] == _TENANT_ID_PARAM
            and posted_data["departureDate"] == "2022-12-20"
        )
        assert mock_connection.post.call_args[0][0] == "v2/departingemployee/add"
        assert mock_connection.post.call_count == 1

    def test_add_when_user_already_on_list_raises_user_already_added_error(
        self, mocker, mock_connection, user_context, mock_detection_list_user_client
    ):
        def side_effect(url, json):
            if "add" in url:
                raise create_mock_error(
                    Py42BadRequestError, mocker, "User already on list"
                )

        mock_connection.post.side_effect = side_effect
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        with pytest.raises(Py42UserAlreadyAddedError) as err:
            client.add("user_id")

        expected = "User with ID user_id is already on the departing-employee list."
        assert str(err.value) == expected

    def test_remove_posts_expected_data_and_to_expected_url(
        self,
        mock_connection,
        user_context,
        mock_get_all_response_empty,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        mock_connection.post.return_value = mock_get_all_response_empty
        client.remove("999")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = mock_connection.post.call_args[1]["json"]
        assert (
            posted_data["userId"] == "999"
            and posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
        )
        assert mock_connection.post.call_args[0][0] == "v2/departingemployee/remove"

    def test_get_all_posts_expected_data_to_expected_url(
        self,
        mock_connection,
        user_context,
        mock_get_all_response,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        mock_connection.post.return_value = mock_get_all_response
        for _ in client.get_all():
            break
        first_call = mock_connection.post.call_args_list[0]
        posted_data = first_call[1]["json"]
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["pgSize"] == 100
            and posted_data["pgNum"] == 1
            and posted_data["filterType"] == "OPEN"
            and posted_data["srtKey"] == "CREATED_AT"
            and posted_data["srtDirection"] == "DESC"
        )
        assert mock_connection.post.call_args[0][0] == "v2/departingemployee/search"
        assert mock_connection.post.call_count == 1

    def test_get_all_posts_expected_data_with_non_default_values(
        self, user_context, mock_connection, mock_detection_list_user_client
    ):
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )

        for _ in client.get_all(
            filter_type="NEW_FILTER",
            sort_direction="DESC",
            sort_key="DISPLAY_NAME",
            page_size=200,
        ):
            break

        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_count == 1
        assert mock_connection.post.call_args[0][0] == "v2/departingemployee/search"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["filterType"] == "NEW_FILTER"
            and posted_data["pgNum"] == 1
            and posted_data["pgSize"] == 200
            and posted_data["srtKey"] == "DISPLAY_NAME"
            and posted_data["srtDirection"] == "DESC"
        )

    def test_get_posts_expected_data_to_expected_url(
        self,
        mock_connection,
        user_context,
        mock_get_all_response_empty,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        mock_connection.post.return_value = mock_get_all_response_empty
        client.get("999")

        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_args[0][0] == "v2/departingemployee/get"
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["userId"] == "999"
        )

    def test_get_page_posts_data_to_expected_url(
        self,
        mock_connection,
        user_context,
        mock_get_all_response,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        client.get_page(
            filter_type="OPEN",
            sort_key="CREATED_AT",
            sort_direction="DESC",
            page_num=1,
            page_size=100,
        )
        mock_connection.post.return_value = mock_get_all_response
        first_call = mock_connection.post.call_args_list[0]
        posted_data = first_call[1]["json"]
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["pgSize"] == 100
            and posted_data["pgNum"] == 1
            and posted_data["filterType"] == "OPEN"
            and posted_data["srtKey"] == "CREATED_AT"
            and posted_data["srtDirection"] == "DESC"
        )
        assert mock_connection.post.call_args[0][0] == "v2/departingemployee/search"
        assert mock_connection.post.call_count == 1

    def test_set_alerts_enabled_posts_expected_data(
        self,
        mock_connection,
        user_context,
        mock_get_all_response_empty,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        mock_connection.post.return_value = mock_get_all_response_empty
        client.set_alerts_enabled()

        posted_data = mock_connection.post.call_args[1]["json"]
        assert (
            posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["alertsEnabled"] is True
        )

    def test_set_alerts_enabled_posts_to_expected_url(
        self,
        mock_connection,
        user_context,
        mock_get_all_response_empty,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        mock_connection.post.return_value = mock_get_all_response_empty
        client.set_alerts_enabled()
        assert (
            mock_connection.post.call_args[0][0] == "v2/departingemployee/setalertstate"
        )

    def test_update_posts_expected_data(
        self,
        mock_connection,
        user_context,
        mock_get_all_response,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        mock_connection.post.return_value = mock_get_all_response
        client.update_departure_date(_USER_ID, "2020-12-20")

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = mock_connection.post.call_args[1]["json"]
        assert (
            posted_data["userId"] == _USER_ID
            and posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["departureDate"] == "2020-12-20"
        )

    def test_update_posts_to_expected_url(
        self, mock_connection, user_context, mock_detection_list_user_client
    ):
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        client.update_departure_date(_USER_ID, "2022-12-20")
        assert mock_connection.post.call_args[0][0] == "v2/departingemployee/update"

    def test_update_posts_expected_data_with_datetime_instance(
        self,
        mock_connection,
        user_context,
        mock_get_all_response,
        mock_detection_list_user_client,
    ):
        client = DepartingEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        mock_connection.post.return_value = mock_get_all_response
        dt = datetime.strptime("2020-12-20", "%Y-%m-%d")
        client.update_departure_date(_USER_ID, dt)

        # Have to convert the request data to a dict because
        # older versions of Python don't have deterministic order.
        posted_data = mock_connection.post.call_args[1]["json"]
        assert (
            posted_data["userId"] == _USER_ID
            and posted_data["tenantId"] == TENANT_ID_FROM_RESPONSE
            and posted_data["departureDate"] == "2020-12-20"
        )

    def test_remove_raises_error_when_user_id_does_not_exist(
        self,
        user_context,
        mock_post_not_found_session,
        mock_detection_list_user_client,
    ):
        departing_employee_client = DepartingEmployeeService(
            mock_post_not_found_session, user_context, mock_detection_list_user_client
        )
        user_id = "942897397520289999"
        with pytest.raises(Py42UserNotOnListError) as err:
            departing_employee_client.remove(user_id)
        assert (
            f"User with ID '{user_id}' is not currently on the departing-employee list."
            in str(err.value)
        )
