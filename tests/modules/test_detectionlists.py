import pytest

from py42._internal.client_factories import MicroserviceClientFactory
from py42._internal.clients.detection_list_user import DetectionListUserClient
from py42.clients.users import UserClient
from py42.modules.detectionlists import DetectionListsModule


@pytest.fixture
def mock_microservice_client_factory(mocker):
    return mocker.MagicMock(spec=MicroserviceClientFactory)


@pytest.fixture
def mock_detection_list_user_client(mocker):
    return mocker.MagicMock(spec=DetectionListUserClient)


@pytest.fixture
def mock_user_client(mocker):
    return mocker.MagicMock(spec=UserClient)


class TestDetectionListModule(object):
    def test_departing_employee_call_get_departing_employee_client_with_expected_values(
        self, mock_microservice_client_factory, mock_user_client
    ):
        module = DetectionListsModule(mock_microservice_client_factory, mock_user_client)
        test = module.departing_employee
        mock_microservice_client_factory.get_departing_employee_client.assert_called_once_with(
            mock_user_client
        )

    def test_high_risk_employee_returns_high_risk_employee_client(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        pass

    def test_create_user_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        pass

    def test_get_user_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        pass

    def test_get_user_by_id_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        pass

    def test_update_user_notes_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        pass

    def test_add_user_risk_tag_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        pass

    def test_remove_user_risk_tag_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        pass

    def test_add_user_cloud_alias_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        pass

    def test_remove_user_cloud_alias_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        pass
