import pytest

from py42.clients.watchlists import WatchlistsClient
from py42.services.watchlists import WatchlistsService

WATCHLIST_ID = "123"
WATCHLIST_TYPE = "DEPARTING_EMPLOYEE"


@pytest.fixture
def mock_watchlists_service(mocker):
    return mocker.MagicMock(spec=WatchlistsService)


class TestWatchlistsClient:
    def test_get_calls_service_with_expected_params(
        self,
        mock_watchlists_service,
    ):
        watchlists_client = WatchlistsClient(mock_watchlists_service)
        watchlists_client.get(WATCHLIST_ID)
        mock_watchlists_service.get.assert_called_once_with(WATCHLIST_ID)

    def test_delete_calls_service_with_expected_params(
        self,
        mock_watchlists_service,
    ):
        watchlists_client = WatchlistsClient(mock_watchlists_service)
        watchlists_client.delete(WATCHLIST_ID)
        mock_watchlists_service.delete.assert_called_once_with(WATCHLIST_ID)

    def test_get_all_calls_service_with_expected_params(
        self,
        mock_watchlists_service,
    ):
        watchlists_client = WatchlistsClient(mock_watchlists_service)
        watchlists_client.get_all()
        assert mock_watchlists_service.get_all.call_count == 1

    def test_create_calls_service_with_expected_params(
        self,
        mock_watchlists_service,
    ):
        watchlists_client = WatchlistsClient(mock_watchlists_service)
        watchlists_client.create(WATCHLIST_TYPE)
        mock_watchlists_service.create.assert_called_once_with(WATCHLIST_TYPE)

    def test_get_all_included_users_calls_service_with_expected_params(
        self, mock_watchlists_service
    ):
        watchlists_client = WatchlistsClient(mock_watchlists_service)
        watchlists_client.get_all_included_users(WATCHLIST_ID)
        mock_watchlists_service.get_all_included_users.assert_called_once_with(
            WATCHLIST_ID
        )

    def test_add_included_users_by_watchlist_id_calls_service_with_expected_params(
        self, mock_watchlists_service
    ):
        watchlists_client = WatchlistsClient(mock_watchlists_service)
        user_ids = ["1a", "2b", "3c"]
        watchlists_client.add_included_users_by_watchlist_id(user_ids, WATCHLIST_ID)
        mock_watchlists_service.add_included_users_by_watchlist_id.assert_called_once_with(
            user_ids, WATCHLIST_ID
        )

    def test_add_included_users_by_watchlist_tyoe_calls_service_with_expected_params(
        self, mock_watchlists_service
    ):
        watchlists_client = WatchlistsClient(mock_watchlists_service)
        user_ids = ["1a", "2b", "3c"]
        watchlists_client.add_included_users_by_watchlist_type(user_ids, WATCHLIST_TYPE)
        mock_watchlists_service.add_included_users_by_watchlist_type.assert_called_once_with(
            user_ids, WATCHLIST_TYPE
        )

    def test_delete_included_users_by_watchlist_id_calls_service_with_expected_params(
        self, mock_watchlists_service
    ):
        watchlists_client = WatchlistsClient(mock_watchlists_service)
        user_ids = ["1a", "2b", "3c"]
        watchlists_client.delete_included_users_by_watchlist_id(user_ids, WATCHLIST_ID)
        mock_watchlists_service.delete_included_users_by_watchlist_id.assert_called_once_with(
            user_ids, WATCHLIST_ID
        )

    def test_delete_included_users_by_watchlist_tyoe_calls_service_with_expected_params(
        self, mock_watchlists_service
    ):
        watchlists_client = WatchlistsClient(mock_watchlists_service)
        user_ids = ["1a", "2b", "3c"]
        watchlists_client.delete_included_users_by_watchlist_type(
            user_ids, WATCHLIST_TYPE
        )
        mock_watchlists_service.delete_included_users_by_watchlist_type.assert_called_once_with(
            user_ids, WATCHLIST_TYPE
        )

    def test_get_watchlist_member_calls_service_with_expected_params(
        self, mock_watchlists_service
    ):
        watchlists_client = WatchlistsClient(mock_watchlists_service)
        watchlists_client.get_watchlist_member(WATCHLIST_ID, "123")
        mock_watchlists_service.get_watchlist_member.assert_called_once_with(
            WATCHLIST_ID, "123"
        )

    def test_get_all_watchlist_members_calls_service_with_expected_params(
        self, mock_watchlists_service
    ):
        watchlists_client = WatchlistsClient(mock_watchlists_service)
        watchlists_client.get_all_watchlist_members(WATCHLIST_ID)
        mock_watchlists_service.get_all_watchlist_members.assert_called_once_with(
            WATCHLIST_ID
        )
