import pytest
import json

from py42.sdk.usercontext import UserContext

from py42.clients.detectionlists.high_risk_employee import HighRiskEmployeeClient

# Validate URL
# Validate post data
# Validate return status and response

CREATE_USER_SAMPLE_RESPONSE = """
    {"type$":"USER_V2","tenantId":"1d71796f-af5b-4231-9d8e-df6434da4663",
    "userId":"942897397520289999",
    "userName":"test.employee@test.com",
    "displayName":"Test Employee",
    "cloudUsernames":["test.employee@test.com"],"riskFactors":[]}
"""


class TestHighRiskEmployeeClient(object):
    @pytest.fixture
    def mock_user_context(self, mocker):
        return mocker.MagicMock(spec=UserContext)

    @pytest.fixture
    def mock_get_tenant_id(self, mocker, mock_user_context):
        # mocker.patch(
        #    "py42.clients.detectionlists.high_risk_employee.HighRiskEmployeeClient._user_context.get_tenant_id"
        # )
        mock_user_context.get_current_tenant_id.return_value = "DUMMY-TENANT-ID"
        return mock_user_context

    @pytest.fixture
    def mock_session_post_success(self, mock_session, py42_response):
        py42_response.status_code = 201
        py42_response.text = CREATE_USER_SAMPLE_RESPONSE
        mock_session.post.return_value = py42_response
        return mock_session

    @pytest.fixture
    def mock_session_post_failure(self, mock_session, py42_response):
        py42_response.status_code = 404
        mock_session.post.return_value = py42_response
        return mock_session

    @pytest.fixture
    def mock_get_by_username(self, mock_session, py42_response):
        py42_response.status_code = 201
        py42_response.text = '{"userId": "abc"}'
        mock_session.post.return_value = py42_response

    def test_create_as_user_does_not_exists_posts_expected_data(
        self, mock_user_context, mock_session_post_success, mock_get_tenant_id
    ):

        high_risk_employee_client = HighRiskEmployeeClient(
            mock_session_post_success, mock_user_context
        )
        high_risk_employee_client.create("test_employee@test.com")

        posted_data = json.loads(mock_session_post_success.post.call_args[1]["data"])

        # Need to assert params to post when _create_user is called
        """
                assert (
                    posted_data["userName"] == "test_employee@test.com"
                    and posted_data["tenantId"] == mock_get_tenant_id
                    and posted_data["notes"] == ""
                    and posted_data["riskFactors"] == []
                    and posted_data["cloudUsernames"] == []
                )
                """

        assert mock_session_post_success.post.call_count == 2
        assert mock_session_post_success.post.call_args[0][0] == "/svc/api/v2/highriskemployee/add"
        assert (
            posted_data["tenantId"] == mock_get_tenant_id.get_current_tenant_id.return_value
            and posted_data["userId"] == "942897397520289999"
        )

        # mock get_tenant_id
        # mock get_by_username fails
        # mock create_user
        # mock add_high_risk_employee
        # validate success status
        # validate optional params

    def test_create_as_user_exists_posts_expected_data(self):
        # mock get_tenant_id
        # mock get_by_username succeeds
        # mock add_high_risk_employee
        # validate success status
        # validate optional params
        pass

    def test_create_fails_as_create_user_failed(self):
        # mock get_tenant_id
        # mock get_by_username fails
        # mock create_user fails
        # add_high_risk_employee is not called
        pass

    def test_create_fails_as_add_high_risk_employee_fails(self):
        # mock get_tenant_id
        # mock get_by_username fails
        # mock create_user
        # add_high_risk_employee fails
        pass

    def test_create_fails_as_add_high_risk_employee_fails_when_user_already_exists(self):
        # mock get_tenant_id
        # mock get_by_username fails
        # mock create_user
        # mock add_high_risk_employee
        pass

    def test_create_fails_as_get_tenant_id_fails(self):
        # mock get_tenant_id fails
        pass

    def test_toggle_alerts_posts_expected_data(self):
        pass

    def test_toggle_alerts_fails(self):
        pass

    def resolve_posts_expected_data(self):
        pass

    def resolve_fails(self):
        pass

    def test_get_by_id_posts_expected_data(self):
        pass

    def test_get_by_id_fails(self):
        pass

    def test_get_by_username_posts_expected_data(self):
        pass

    def test_get_by_username_fails(self):
        pass

    def test_get_all_posts_expected_data(self):
        pass

    def test_get_all_fails(self):
        pass
