import pytest

from py42.clients.trustedactivities import TrustedActivitiesClient
from py42.services.trustedactivities import TrustedActivitiesService


_TEST_TRUSTED_ACTIVITY_RESOURCE_ID = 123


@pytest.fixture
def mock_trusted_activities_service(mocker):
    return mocker.MagicMock(spec=TrustedActivitiesService)


class TestTrustedActivitiesClient:
    def test_get_all_calls_service_with_expected_params(self, mock_trusted_activities_service):
        trusted_activities_client = TrustedActivitiesClient(mock_trusted_activities_service)
        trusted_activities_client.get_all()
        assert mock_trusted_activities_service.get_all.call_count == 1

    def test_create_calls_service_with_expected_params(self, mock_trusted_activities_service):
        trusted_activities_client = TrustedActivitiesClient(mock_trusted_activities_service)
        trusted_activities_client.create(
            "DOMAIN",
            "test.com",
            description="description"
        )
        mock_trusted_activities_service.create.assert_called_once_with(
            "DOMAIN",
            "test.com",
            "description"
        )

    def test_get_calls_service_with_expected_params(self, mock_trusted_activities_service):
        trusted_activities_client = TrustedActivitiesClient(mock_trusted_activities_service)
        trusted_activities_client.get(_TEST_TRUSTED_ACTIVITY_RESOURCE_ID)
        mock_trusted_activities_service.get.assert_called_once_with(_TEST_TRUSTED_ACTIVITY_RESOURCE_ID)

    def test_update_calls_service_with_expected_params(self, mock_trusted_activities_service):
        trusted_activities_client = TrustedActivitiesClient(mock_trusted_activities_service)
        trusted_activities_client.update(
            _TEST_TRUSTED_ACTIVITY_RESOURCE_ID,
            value="new-domain.com")
        mock_trusted_activities_service.update.assert_called_once_with(
            id=_TEST_TRUSTED_ACTIVITY_RESOURCE_ID,
            type=None,
            value="new-domain.com",
            description=None,
        )

    def test_delete_calls_service_with_expected_params(self, mock_trusted_activities_service):
        trusted_activities_client = TrustedActivitiesClient(mock_trusted_activities_service)
        trusted_activities_client.delete(_TEST_TRUSTED_ACTIVITY_RESOURCE_ID)
        mock_trusted_activities_service.delete.assert_called_once_with(_TEST_TRUSTED_ACTIVITY_RESOURCE_ID)
