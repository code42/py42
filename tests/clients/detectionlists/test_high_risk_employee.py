import json

import pytest
from requests import HTTPError
from requests import Response

from py42._internal.clients.detection_list_user import DetectionListUserClient
from py42.clients.detectionlists.high_risk_employee import HighRiskEmployeeClient
from py42.clients.detectionlists.high_risk_employee import HighRiskEmployeeFilters
from py42.clients.users import UserClient
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42UserAlreadyAddedError

CREATE_USER_SAMPLE_RESPONSE = """
    {"type$":"USER_V2","tenantId":"1d71796f-af5b-4231-9d8e-df6434da4663",
    "userId":"942897397520289999",
    "userName":"test.employee@example.com",
    "displayName":"Test Employee",
    "cloudUsernames":["test.employee@test.com"],"riskFactors":[]}
"""


class TestHighRiskEmployeeFilters(object):
    def test_choices_are_correct(self):
        actual = HighRiskEmployeeFilters.choices()
        expected = ["OPEN", "EXFILTRATION_24_HOURS", "EXFILTRATION_30_DAYS"]
        assert set(actual) == set(expected)


class TestHighRiskEmployeeClient(object):
    @pytest.fixture
    def mock_session_post_success(self, mock_session, py42_response):
        py42_response.status_code = 201
        py42_response.text = CREATE_USER_SAMPLE_RESPONSE
        mock_session.post.return_value = py42_response
        return mock_session

    @pytest.fixture
    def mock_user_client(self, mock_session, user_context, py42_response):
        user_client = UserClient(mock_session)
        mock_session.post.return_value = py42_response
        return user_client

    @pytest.fixture
    def mock_detection_list_user_client(
        self, mock_session, user_context, py42_response, mock_user_client
    ):
        user_client = DetectionListUserClient(
            mock_session, user_context, mock_user_client
        )
        mock_session.post.return_value = py42_response
        return user_client

    def test_add_posts_expected_data(
        self, user_context, mock_session_post_success, mock_detection_list_user_client
    ):
        high_risk_employee_client = HighRiskEmployeeClient(
            mock_session_post_success, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.add("942897397520289999")

        posted_data = json.loads(mock_session_post_success.post.call_args[1]["data"])
        assert mock_session_post_success.post.call_count == 2
        assert (
            mock_session_post_success.post.call_args[0][0]
            == "/svc/api/v2/highriskemployee/add"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
        )

    def test_add_when_user_already_on_list_raises_user_already_added_error(
        self, mocker, mock_session, user_context, mock_detection_list_user_client
    ):
        def side_effect(url, data):
            if "add" in url:
                base_err = mocker.MagicMock(spec=HTTPError)
                base_err.response = mocker.MagicMock(spec=Response)
                base_err.response.text = "User already on list"
                raise Py42BadRequestError(base_err)

        mock_session.post.side_effect = side_effect
        client = HighRiskEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        with pytest.raises(Py42UserAlreadyAddedError) as err:
            client.add("user_id")

        expected = "User with ID user_id is already on the high-risk-employee list."
        assert str(err.value) == expected

    def test_set_alerts_enabled_posts_expected_data_with_default_value(
        self, user_context, mock_session, mock_detection_list_user_client
    ):
        high_risk_employee_client = HighRiskEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.set_alerts_enabled()

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert (
            mock_session.post.call_args[0][0]
            == "/svc/api/v2/highriskemployee/setalertstate"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["alertsEnabled"] is True
        )

    def test_set_alerts_enabled_posts_expected_data(
        self, user_context, mock_session, mock_detection_list_user_client
    ):
        high_risk_employee_client = HighRiskEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.set_alerts_enabled(False)

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert (
            mock_session.post.call_args[0][0]
            == "/svc/api/v2/highriskemployee/setalertstate"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["alertsEnabled"] is False
        )

    def test_remove_posts_expected_data(
        self, user_context, mock_session, mock_detection_list_user_client
    ):
        high_risk_employee_client = HighRiskEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.remove("942897397520289999")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])

        assert mock_session.post.call_count == 1
        assert (
            mock_session.post.call_args[0][0] == "/svc/api/v2/highriskemployee/remove"
        )
        assert posted_data["tenantId"] == user_context.get_current_tenant_id()
        assert posted_data["userId"] == "942897397520289999"

    def test_get_posts_expected_data(
        self,
        user_context,
        mock_session,
        mock_detection_list_user_client,
        mock_user_client,
    ):
        high_risk_employee_client = HighRiskEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.get("942897397520289999")

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert mock_session.post.call_args[0][0] == "/svc/api/v2/highriskemployee/get"
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["userId"] == "942897397520289999"
        )

    def test_get_all_posts_expected_data(
        self,
        user_context,
        mock_session,
        mock_detection_list_user_client,
        mock_user_client,
    ):
        high_risk_employee_client = HighRiskEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        for _ in high_risk_employee_client.get_all():
            break

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert (
            mock_session.post.call_args[0][0] == "/svc/api/v2/highriskemployee/search"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["filterType"] == "OPEN"
            and posted_data["pgNum"] == 1
            and posted_data["pgSize"] == 100
            and posted_data["srtKey"] is None
            and posted_data["srtDirection"] is None
        )

    def test_get_all_posts_expected_data_with_non_default_values(
        self, user_context, mock_session, mock_detection_list_user_client
    ):
        high_risk_employee_client = HighRiskEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        for _ in high_risk_employee_client.get_all(
            filter_type="NEW_FILTER", sort_direction="DESC", sort_key="DISPLAY_NAME"
        ):
            break

        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert (
            mock_session.post.call_args[0][0] == "/svc/api/v2/highriskemployee/search"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["filterType"] == "NEW_FILTER"
            and posted_data["pgNum"] == 1
            and posted_data["pgSize"] == 100
            and posted_data["srtKey"] == "DISPLAY_NAME"
            and posted_data["srtDirection"] == "DESC"
        )

    def test_get_page_posts_data_to_expected_url(
        self, user_context, mock_session, mock_detection_list_user_client
    ):
        high_risk_employee_client = HighRiskEmployeeClient(
            mock_session, user_context, mock_detection_list_user_client
        )
        high_risk_employee_client.get_page(
            filter_type="NEW_FILTER",
            page_num=3,
            page_size=10,
            sort_direction="DESC",
            sort_key="DISPLAY_NAME",
        )
        posted_data = json.loads(mock_session.post.call_args[1]["data"])
        assert mock_session.post.call_count == 1
        assert (
            mock_session.post.call_args[0][0] == "/svc/api/v2/highriskemployee/search"
        )
        assert (
            posted_data["tenantId"] == user_context.get_current_tenant_id()
            and posted_data["filterType"] == "NEW_FILTER"
            and posted_data["pgNum"] == 3
            and posted_data["pgSize"] == 10
            and posted_data["srtKey"] == "DISPLAY_NAME"
            and posted_data["srtDirection"] == "DESC"
        )
