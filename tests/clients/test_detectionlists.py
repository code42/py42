import pytest

from py42.clients.detectionlists import DetectionListsClient
from py42.clients.detectionlists import RiskTags
from py42.services.detectionlists._profile import DetectionListUserService
from py42.services.detectionlists.departing_employee import DepartingEmployeeService
from py42.services.detectionlists.high_risk_employee import HighRiskEmployeeService


@pytest.fixture
def mock_detection_list_user_service(mocker):
    return mocker.MagicMock(spec=DetectionListUserService)


@pytest.fixture
def mock_departing_employee_service(mocker):
    return mocker.MagicMock(spec=DepartingEmployeeService)


@pytest.fixture
def mock_high_risk_employee_service(mocker):
    return mocker.MagicMock(spec=HighRiskEmployeeService)


TEST_USER_ID = "12345"


class TestRiskTags(object):
    def test_choices_returns_expected_set(self):
        choices = RiskTags.choices()
        valid_set = {
            "FLIGHT_RISK",
            "HIGH_IMPACT_EMPLOYEE",
            "ELEVATED_ACCESS_PRIVILEGES",
            "PERFORMANCE_CONCERNS",
            "SUSPICIOUS_SYSTEM_ACTIVITY",
            "POOR_SECURITY_PRACTICES",
            "CONTRACT_EMPLOYEE",
        }
        assert set(choices) == valid_set


class TestDetectionListClient(object):
    def test_departing_employee_call_get_departing_employee_client_with_expected_values(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        assert module.departing_employee is mock_departing_employee_service

    def test_high_risk_employee_returns_high_risk_employee_client(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        assert module.high_risk_employee is mock_high_risk_employee_service

    def test_create_user_calls_user_client_with_expected_values(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        module.create_user("testusername")
        mock_detection_list_user_service.create.assert_called_once_with("testusername")

    def test_get_user_calls_user_client_with_expected_values(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        module.get_user("testusername")
        mock_detection_list_user_service.get.assert_called_once_with("testusername")

    def test_get_user_by_id_calls_user_client_with_expected_values(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        module.get_user_by_id(TEST_USER_ID)
        mock_detection_list_user_service.get_by_id.assert_called_once_with(TEST_USER_ID)

    def test_update_user_notes_calls_user_client_with_expected_values(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        module.update_user_notes(TEST_USER_ID, "newnotes")
        mock_detection_list_user_service.update_notes.assert_called_once_with(
            TEST_USER_ID, "newnotes"
        )

    def test_update_user_notes_returns_response(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        response = module.update_user_notes(TEST_USER_ID, "newnotes")
        assert response

    def test_add_user_risk_tags_calls_user_client_with_expected_values(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        module.add_user_risk_tags(TEST_USER_ID, "newtag")
        mock_detection_list_user_service.add_risk_tags.assert_called_once_with(
            TEST_USER_ID, "newtag"
        )

    def test_add_user_risk_tags_returns_response(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        response = module.add_user_risk_tags(TEST_USER_ID, "newtag")
        assert response

    def test_remove_user_risk_tags_calls_user_client_with_expected_values(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        module.remove_user_risk_tags(TEST_USER_ID, "oldtag")
        mock_detection_list_user_service.remove_risk_tags.assert_called_once_with(
            TEST_USER_ID, "oldtag"
        )

    def test_remove_user_risk_tags_returns_response(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        response = module.remove_user_risk_tags(TEST_USER_ID, "oldtag")
        assert response

    def test_add_user_cloud_alias_calls_user_client_with_expected_values(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        module.add_user_cloud_alias(TEST_USER_ID, "newalias")
        mock_detection_list_user_service.add_cloud_alias.assert_called_once_with(
            TEST_USER_ID, "newalias"
        )

    def test_add_user_cloud_alias_returns_response(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        response = module.add_user_cloud_alias(TEST_USER_ID, "newalias")
        assert response

    def test_remove_user_cloud_alias_calls_user_client_with_expected_values(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        module.remove_user_cloud_alias(TEST_USER_ID, "oldalias")
        mock_detection_list_user_service.remove_cloud_alias.assert_called_once_with(
            TEST_USER_ID, "oldalias"
        )

    def test_remove_user_cloud_alias_returns_response(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        response = module.remove_user_cloud_alias(TEST_USER_ID, "oldalias")
        assert response

    def test_refresh_user_scim_attributes_calls_user_client_with_expected_values(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        module.refresh_user_scim_attributes(TEST_USER_ID)
        mock_detection_list_user_service.refresh.assert_called_once_with(TEST_USER_ID)

    def test_refresh_user_scim_attributes_returns_response(
        self,
        mock_detection_list_user_service,
        mock_departing_employee_service,
        mock_high_risk_employee_service,
    ):
        module = DetectionListsClient(
            mock_detection_list_user_service,
            mock_departing_employee_service,
            mock_high_risk_employee_service,
        )
        response = module.refresh_user_scim_attributes(TEST_USER_ID)
        assert response
