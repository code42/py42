import pytest

from py42.clients.userriskprofile import UserRiskProfileClient
from py42.services.userriskprofile import UserRiskProfileService


USER_ID = "123"
USERNAME = "risk-user@code42.com"


@pytest.fixture
def mock_user_risk_profile_service(mocker):
    return mocker.MagicMock(spec=UserRiskProfileService)


class TestUserRiskProfileClient:
    def test_get_by_id_calls_service_with_expected_params(
        self, mock_user_risk_profile_service
    ):
        user_risk_profile_client = UserRiskProfileClient(mock_user_risk_profile_service)
        user_risk_profile_client.get_by_id(USER_ID)
        mock_user_risk_profile_service.get_by_id.assert_called_once_with(USER_ID)

    def test_get_by_username_calls_service_with_expected_params(
        self, mock_user_risk_profile_service
    ):
        user_risk_profile_client = UserRiskProfileClient(mock_user_risk_profile_service)
        user_risk_profile_client.get_by_username(USERNAME)
        mock_user_risk_profile_service.get_by_username.assert_called_once_with(USERNAME)

    def test_update_calls_service_with_expected_params(
        self, mock_user_risk_profile_service
    ):
        user_risk_profile_client = UserRiskProfileClient(mock_user_risk_profile_service)
        user_risk_profile_client.update(USER_ID)
        mock_user_risk_profile_service.update.assert_called_once_with(
            USER_ID, None, None, None
        )

    def test_update_calls_service_with_optional_params(
        self, mock_user_risk_profile_service
    ):
        user_risk_profile_client = UserRiskProfileClient(mock_user_risk_profile_service)
        user_risk_profile_client.update(USER_ID, "2022-1-1", "2022-4-1", "notes")
        mock_user_risk_profile_service.update.assert_called_once_with(
            USER_ID, "2022-1-1", "2022-4-1", "notes"
        )

    def test_get_page_calls_service_with_expected_params(
        self, mock_user_risk_profile_service
    ):
        user_risk_profile_client = UserRiskProfileClient(mock_user_risk_profile_service)
        user_risk_profile_client.get_page()
        assert mock_user_risk_profile_service.get_page.call_count == 1

    def test_get_page_calls_service_with_optional_params(
        self, mock_user_risk_profile_service
    ):
        user_risk_profile_client = UserRiskProfileClient(mock_user_risk_profile_service)
        user_risk_profile_client.get_page(page_num=1, page_size=10)
        mock_user_risk_profile_service.get_page.assert_called_once_with(
            1, 10, None, None, None, None, None, None, None, None, None, None, None
        )

    def test_get_all_calls_service_with_expected_params(
        self, mock_user_risk_profile_service
    ):
        user_risk_profile_client = UserRiskProfileClient(mock_user_risk_profile_service)
        user_risk_profile_client.get_all()
        assert mock_user_risk_profile_service.get_all.call_count == 1

    def test_get_all_calls_service_with_optional_params(
        self, mock_user_risk_profile_service
    ):
        user_risk_profile_client = UserRiskProfileClient(mock_user_risk_profile_service)
        user_risk_profile_client.get_all(
            manager_id="manager-id",
            title="engineer",
            division="division",
            department="prod",
            employment_type="full-time",
            country="usa",
            region="midwest",
            locality="local",
            active=True,
            deleted=False,
            support_user=False,
        )
        mock_user_risk_profile_service.get_all.assert_called_once_with(
            "manager-id",
            "engineer",
            "division",
            "prod",
            "full-time",
            "usa",
            "midwest",
            "local",
            True,
            False,
            False,
        )

    def test_add_cloud_aliases_calls_service_with_expected_params(
        self, mock_user_risk_profile_service
    ):
        user_risk_profile_client = UserRiskProfileClient(mock_user_risk_profile_service)
        user_risk_profile_client.add_cloud_aliases(USER_ID, "cloud-alias@email.com")
        mock_user_risk_profile_service.add_cloud_aliases.assert_called_once_with(
            USER_ID, "cloud-alias@email.com"
        )

    def test_delete_cloud_aliases_calls_service_with_expected_params(
        self, mock_user_risk_profile_service
    ):
        aliases = ["cloud-alias@email.com", "default@code42.com"]
        user_risk_profile_client = UserRiskProfileClient(mock_user_risk_profile_service)
        user_risk_profile_client.delete_cloud_aliases(USER_ID, aliases)
        mock_user_risk_profile_service.delete_cloud_aliases(USER_ID, aliases)
