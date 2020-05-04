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


TEST_USER_ID = "12345"


class TestDetectionListModule(object):
    def test_departing_employee_call_get_departing_employee_client_with_expected_values(
        self, mock_microservice_client_factory, mock_user_client
    ):
        module = DetectionListsModule(mock_microservice_client_factory)
        _ = module.departing_employee
        assert mock_microservice_client_factory.get_departing_employee_client.call_count

    def test_high_risk_employee_returns_high_risk_employee_client(
        self, mock_microservice_client_factory, mock_user_client
    ):
        module = DetectionListsModule(mock_microservice_client_factory)
        _ = module.high_risk_employee
        assert mock_microservice_client_factory.get_high_risk_employee_client.call_count

    def test_create_user_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        mock_microservice_client_factory.get_detection_list_user_client.return_value = (
            mock_detection_list_user_client
        )
        module = DetectionListsModule(mock_microservice_client_factory)
        module.create_user("testusername")
        mock_detection_list_user_client.create.assert_called_once_with("testusername")

    def test_get_user_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        mock_microservice_client_factory.get_detection_list_user_client.return_value = (
            mock_detection_list_user_client
        )
        module = DetectionListsModule(mock_microservice_client_factory)
        module.get_user("testusername")
        mock_detection_list_user_client.get.assert_called_once_with("testusername")

    def test_get_user_by_id_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        mock_microservice_client_factory.get_detection_list_user_client.return_value = (
            mock_detection_list_user_client
        )
        module = DetectionListsModule(mock_microservice_client_factory)
        module.get_user_by_id(TEST_USER_ID)
        mock_detection_list_user_client.get_by_id.assert_called_once_with(TEST_USER_ID)

    def test_update_user_notes_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        mock_microservice_client_factory.get_detection_list_user_client.return_value = (
            mock_detection_list_user_client
        )
        module = DetectionListsModule(mock_microservice_client_factory)
        module.update_user_notes(TEST_USER_ID, "newnotes")
        mock_detection_list_user_client.update_notes.assert_called_once_with(
            TEST_USER_ID, "newnotes"
        )

    def test_add_user_risk_tag_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        mock_microservice_client_factory.get_detection_list_user_client.return_value = (
            mock_detection_list_user_client
        )
        module = DetectionListsModule(mock_microservice_client_factory)
        module.add_user_risk_tags(TEST_USER_ID, "newtag")
        mock_detection_list_user_client.add_risk_tags.assert_called_once_with(
            TEST_USER_ID, "newtag"
        )

    def test_remove_user_risk_tag_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        mock_microservice_client_factory.get_detection_list_user_client.return_value = (
            mock_detection_list_user_client
        )
        module = DetectionListsModule(mock_microservice_client_factory)
        module.remove_user_risk_tags(TEST_USER_ID, "oldtag")
        mock_detection_list_user_client.remove_risk_tags.assert_called_once_with(
            TEST_USER_ID, "oldtag"
        )

    def test_add_user_cloud_alias_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        mock_microservice_client_factory.get_detection_list_user_client.return_value = (
            mock_detection_list_user_client
        )
        module = DetectionListsModule(mock_microservice_client_factory)
        module.add_user_cloud_alias(TEST_USER_ID, "newalias")
        mock_detection_list_user_client.add_cloud_alias.assert_called_once_with(
            TEST_USER_ID, "newalias"
        )

    def test_remove_user_cloud_alias_calls_user_client_with_expected_values(
        self, mock_microservice_client_factory, mock_detection_list_user_client, mock_user_client
    ):
        mock_microservice_client_factory.get_detection_list_user_client.return_value = (
            mock_detection_list_user_client
        )
        module = DetectionListsModule(mock_microservice_client_factory)
        module.remove_user_cloud_alias(TEST_USER_ID, "oldalias")
        mock_detection_list_user_client.remove_cloud_alias.assert_called_once_with(
            TEST_USER_ID, "oldalias"
        )
