import pytest
from tests.conftest import create_mock_error
from tests.conftest import create_mock_response

from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42UserAlreadyAddedError
from py42.services.detectionlists.high_risk_employee import HighRiskEmployeeFilters
from py42.services.detectionlists.high_risk_employee import HighRiskEmployeeService
from py42.services.detectionlists.user_profile import DetectionListUserService
from py42.services.users import UserService

CREATE_USER_SAMPLE_RESPONSE = """
    {"type$":"USER_V2","tenantId":"1d71796f-af5b-4231-9d8e-df6434da4663",
    "userId":"942897397520289999",
    "userName":"test.employee@example.com",
    "displayName":"Test Employee",
    "cloudUsernames":["test.employee@test.com"],"riskFactors":[]}
"""


class TestHighRiskEmployeeFilters:
    def test_choices_are_correct(self):
        actual = HighRiskEmployeeFilters.choices()
        expected = ["OPEN", "EXFILTRATION_24_HOURS", "EXFILTRATION_30_DAYS"]
        assert set(actual) == set(expected)


class TestHighRiskEmployeeClient:
    @pytest.fixture
    def mock_connection_post_success(self, mock_connection, mocker):
        response = create_mock_response(mocker, CREATE_USER_SAMPLE_RESPONSE, 201)
        mock_connection.post.return_value = response
        return mock_connection

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

    def test_add_posts_expected_data(
        self,
        user_context,
        mock_connection_post_success,
        mock_detection_list_user_client,
    ):
        high_risk_employee_client = HighRiskEmployeeService(
            mock_connection_post_success, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.add("942897397520289999")

        posted_data = mock_connection_post_success.post.call_args[1]["json"]
        assert mock_connection_post_success.post.call_count == 1
        assert (
            mock_connection_post_success.post.call_args[0][0]
            == "v2/highriskemployee/add"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
        )

    def test_add_when_user_already_on_list_raises_user_already_added_error(
        self, mocker, mock_connection, user_context, mock_detection_list_user_client
    ):
        def side_effect(url, json):
            if "add" in url:
                raise create_mock_error(
                    Py42BadRequestError, mocker, "User already on list"
                )

        mock_connection.post.side_effect = side_effect
        client = HighRiskEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        with pytest.raises(Py42UserAlreadyAddedError) as err:
            client.add("user_id")

        expected = "User with ID user_id is already on the high-risk-employee list."
        assert expected in str(err.value)
        assert err.value.user_id == "user_id"

    def test_set_alerts_enabled_posts_expected_data_with_default_value(
        self, user_context, mock_connection, mock_detection_list_user_client
    ):
        high_risk_employee_client = HighRiskEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.set_alerts_enabled()

        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_count == 1
        assert (
            mock_connection.post.call_args[0][0] == "v2/highriskemployee/setalertstate"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["alertsEnabled"] is True
        )

    def test_set_alerts_enabled_posts_expected_data(
        self, user_context, mock_connection, mock_detection_list_user_client
    ):
        high_risk_employee_client = HighRiskEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.set_alerts_enabled(False)

        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_count == 1
        assert (
            mock_connection.post.call_args[0][0] == "v2/highriskemployee/setalertstate"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["alertsEnabled"] is False
        )

    def test_remove_posts_expected_data(
        self, user_context, mock_connection, mock_detection_list_user_client
    ):
        high_risk_employee_client = HighRiskEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.remove("942897397520289999")

        posted_data = mock_connection.post.call_args[1]["json"]

        assert mock_connection.post.call_count == 1
        assert mock_connection.post.call_args[0][0] == "v2/highriskemployee/remove"
        assert posted_data["tenantId"] == user_context.get_current_tenant_id()
        assert posted_data["userId"] == "942897397520289999"

    def test_get_posts_expected_data(
        self,
        user_context,
        mock_connection,
        mock_detection_list_user_client,
    ):
        high_risk_employee_client = HighRiskEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.get("942897397520289999")

        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_count == 1
        assert mock_connection.post.call_args[0][0] == "v2/highriskemployee/get"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
        )

    def test_get_all_posts_expected_data(
        self,
        user_context,
        mock_connection,
        mock_detection_list_user_client,
    ):
        high_risk_employee_client = HighRiskEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        for _ in high_risk_employee_client.get_all():
            break

        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_count == 1
        assert mock_connection.post.call_args[0][0] == "v2/highriskemployee/search"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["filterType"] == "OPEN"
            and posted_data["pgNum"] == 1
            and posted_data["pgSize"] == 100
            and posted_data["srtKey"] is None
            and posted_data["srtDirection"] is None
        )

    def test_get_all_posts_expected_data_with_non_default_values(
        self, user_context, mock_connection, mock_detection_list_user_client
    ):
        high_risk_employee_client = HighRiskEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        for _ in high_risk_employee_client.get_all(
            filter_type="NEW_FILTER",
            sort_direction="DESC",
            sort_key="DISPLAY_NAME",
            page_size=200,
        ):
            break

        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_count == 1
        assert mock_connection.post.call_args[0][0] == "v2/highriskemployee/search"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["filterType"] == "NEW_FILTER"
            and posted_data["pgNum"] == 1
            and posted_data["pgSize"] == 200
            and posted_data["srtKey"] == "DISPLAY_NAME"
            and posted_data["srtDirection"] == "DESC"
        )

    def test_get_page_posts_data_to_expected_url(
        self, user_context, mock_connection, mock_detection_list_user_client
    ):
        high_risk_employee_client = HighRiskEmployeeService(
            mock_connection, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.get_page(
            filter_type="NEW_FILTER",
            page_num=3,
            page_size=10,
            sort_direction="DESC",
            sort_key="DISPLAY_NAME",
        )
        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_count == 1
        assert mock_connection.post.call_args[0][0] == "v2/highriskemployee/search"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["filterType"] == "NEW_FILTER"
            and posted_data["pgNum"] == 3
            and posted_data["pgSize"] == 10
            and posted_data["srtKey"] == "DISPLAY_NAME"
            and posted_data["srtDirection"] == "DESC"
        )

    def test_remove_raises_error_when_user_id_does_not_exist(
        self,
        user_context,
        mock_post_not_found_session,
        mock_detection_list_user_client,
    ):
        high_risk_employee_client = HighRiskEmployeeService(
            mock_post_not_found_session, user_context, mock_detection_list_user_client
        )
        user_id = "942897397520289999"
        with pytest.raises(Py42NotFoundError) as err:
            high_risk_employee_client.remove(user_id)
        assert (
            f"User with ID '{user_id}' is not currently on the high-risk-employee list."
            in str(err.value)
        )
