import json

import pytest
from requests import Response
from tests.conftest import create_mock_error
from tests.conftest import create_mock_response

import py42.settings
from py42.clients.watchlists import WatchlistType
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42Error
from py42.exceptions import Py42InvalidWatchlistType
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42WatchlistNotFound
from py42.exceptions import Py42WatchlistOrUserNotFound
from py42.response import Py42Response
from py42.services.watchlists import WatchlistsService

WATCHLIST_ID = "42-code-123"
WATCHLIST_TYPE = "DEPARTING_EMPLOYEE"
GET_ALL_RESPONSE = '{"watchlists":["test"], "totalCount":1}'
GET_ALL_RESPONSE_EMPTY = '{"watchlists": [], "totalCount":0}'
GET_ALL_INCLUDED_USERS_RESPONSE = '{"includedUsers":["test"], "totalCount":1}'
GET_ALL_INCLUDED_USERS_RESPONSE_EMPTY = '{"includedUsers": [], "totalCount":0}'
GET_ALL_MEMBERS_RESPONSE = '{"watchlistMembers":["test"], "totalCount":2}'
GET_ALL_MEMBERS_RESPONSE_EMPTY = '{"watchlistMembers": [], "totalCount":0}'
WATCHLIST_RESPONSE = {
    "listType": WATCHLIST_TYPE,
    "stats": {"includedUsersCount": 0},
    "tenantId": "1-tenant",
    "watchlistId": WATCHLIST_ID,
}

URI = "/v1/watchlists"


@pytest.fixture
def mock_not_found_error(mocker):
    return create_mock_error(Py42NotFoundError, mocker, "Not Found Error Msg")


@pytest.fixture
def mock_user_not_found_error(mocker):
    return create_mock_error(Py42BadRequestError, mocker, "User not found")


@pytest.fixture
def mock_watchlist_not_found_error(mocker):
    return create_mock_error(Py42BadRequestError, mocker, "Watchlist not found")


@pytest.fixture
def mock_get_all_included_users_response(mocker):
    return create_mock_response(mocker, GET_ALL_INCLUDED_USERS_RESPONSE)


@pytest.fixture
def mock_get_all_included_users_response_empty(mocker):
    return create_mock_response(mocker, GET_ALL_INCLUDED_USERS_RESPONSE_EMPTY)


@pytest.fixture
def mock_get_all_members_response(mocker):
    return create_mock_response(mocker, GET_ALL_MEMBERS_RESPONSE)


@pytest.fixture
def mock_get_all_members_response_empty(mocker):
    return create_mock_response(mocker, GET_ALL_MEMBERS_RESPONSE_EMPTY)


@pytest.fixture
def mock_get_all_response(mocker):
    return create_mock_response(mocker, GET_ALL_RESPONSE)


@pytest.fixture
def mock_get_all_response_empty(mocker):
    return create_mock_response(mocker, GET_ALL_RESPONSE_EMPTY)


class TestWatchlistsService:
    def test_get_calls_get_with_expected_params(self, mock_connection):
        watchlists_service = WatchlistsService(mock_connection)
        watchlists_service.get(WATCHLIST_ID)
        mock_connection.get.assert_called_once_with(f"{URI}/{WATCHLIST_ID}")

    def test_get_raises_py42_not_found_when_id_not_found(
        self, mock_connection, mock_not_found_error
    ):
        watchlists_service = WatchlistsService(mock_connection)
        mock_connection.get.side_effect = mock_not_found_error
        with pytest.raises(Py42WatchlistNotFound) as err:
            watchlists_service.get("invalid-id")

        assert err.value.args[0] == "Watchlist ID 'invalid-id' not found."

    def test_delete_calls_delete_with_expected_params_and_updates_dict(
        self, mock_connection, mocker
    ):
        watchlists_service = WatchlistsService(mock_connection)
        watchlists_service._watchlist_type_id_map = {}
        watchlists_service.watchlist_type_id_map[WATCHLIST_TYPE] = WATCHLIST_ID

        # mock delete response
        requests_response = mocker.MagicMock(spec=Response)
        requests_response.text = json.dumps(WATCHLIST_RESPONSE)
        type(requests_response).status_code = mocker.PropertyMock(return_value=200)
        mock_connection.delete.return_value = Py42Response(requests_response)

        watchlists_service.delete(WATCHLIST_ID)
        mock_connection.delete.assert_called_once_with(f"{URI}/{WATCHLIST_ID}")
        assert WATCHLIST_TYPE not in watchlists_service.watchlist_type_id_map

    def test_delete_raises_py42_not_found_when_id_not_found(
        self, mock_connection, mock_not_found_error
    ):
        watchlists_service = WatchlistsService(mock_connection)
        mock_connection.delete.side_effect = mock_not_found_error
        with pytest.raises(Py42WatchlistNotFound) as err:
            watchlists_service.delete("invalid-id")

        assert err.value.args[0] == "Watchlist ID 'invalid-id' not found."

    def test_get_page_calls_get_with_expected_params(self, mock_connection):
        watchlists_service = WatchlistsService(mock_connection)
        watchlists_service.get_page()
        mock_connection.get.assert_called_once_with(
            URI, params={"page": 1, "page_size": None}
        )

    def test_get_page_calls_get_with_optional_params(self, mock_connection):
        watchlists_service = WatchlistsService(mock_connection)
        watchlists_service.get_page(page_num=1, page_size=10)
        data = {
            "page": 1,
            "page_size": 10,
        }
        mock_connection.get.assert_called_once_with(URI, params=data)

    def test_get_all_calls_get_page_expected_number_of_times(
        self, mock_connection, mock_get_all_response, mock_get_all_response_empty
    ):
        watchlists_service = WatchlistsService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_response,
            mock_get_all_response,
            mock_get_all_response_empty,
        ]

        py42.settings.items_per_page = 1
        for _ in watchlists_service.get_all():
            pass
        py42.settings.items_per_page = 500

        assert mock_connection.get.call_count == 3

    def test_create_calls_post_with_expected_params_and_updates_dictionary(
        self, mocker, mock_connection
    ):
        watchlists_service = WatchlistsService(mock_connection)
        watchlists_service._watchlist_type_id_map = {}

        # mock create call response
        requests_response = mocker.MagicMock(spec=Response)
        requests_response.text = json.dumps(WATCHLIST_RESPONSE)
        mock_connection.post.return_value = Py42Response(requests_response)

        watchlists_service.create(WatchlistType.DEPARTING)

        mock_connection.post.assert_called_once_with(
            URI, json={"watchlistType": "DEPARTING_EMPLOYEE"}
        )
        assert (
            watchlists_service.watchlist_type_id_map["DEPARTING_EMPLOYEE"]
            == WATCHLIST_ID
        )

    def test_create_raises_py42_invalid_type_when_invalid_watchlist_type(
        self, mock_connection, mocker
    ):
        watchlists_service = WatchlistsService(mock_connection)
        mock_invalid_type_error = create_mock_error(
            Py42BadRequestError,
            mocker,
            "Error converting value \\\"INVALID-WATCHLIST-TYPE\\\" to type 'WatchlistSdk.Model.WatchlistType'.",
        )
        mock_connection.post.side_effect = mock_invalid_type_error
        with pytest.raises(Py42InvalidWatchlistType) as err:
            watchlists_service.create("INVALID-WATCHLIST-TYPE")

        assert (
            "'INVALID-WATCHLIST-TYPE' cannot be converted to a valid watchlist type"
            in err.value.args[0]
        )

    def test_get_page_included_users_calls_get_with_expected_params(
        self, mock_connection
    ):
        watchlists_service = WatchlistsService(mock_connection)
        watchlists_service.get_page_included_users(WATCHLIST_ID)
        data = {"page": 1, "page_size": None}
        mock_connection.get.assert_called_once_with(
            f"{URI}/{WATCHLIST_ID}/included-users", params=data
        )

    def test_get_page_included_users_calls_get_with_optional_params(
        self, mock_connection
    ):

        watchlists_service = WatchlistsService(mock_connection)
        watchlists_service.get_page_included_users(WATCHLIST_ID, 1, 10)
        data = {
            "page": 1,
            "page_size": 10,
        }
        mock_connection.get.assert_called_once_with(
            f"{URI}/{WATCHLIST_ID}/included-users", params=data
        )

    def test_get_all_included_users_calls_get_page_expected_number_of_times(
        self,
        mock_connection,
        mock_get_all_included_users_response,
        mock_get_all_included_users_response_empty,
    ):
        watchlists_service = WatchlistsService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_included_users_response,
            mock_get_all_included_users_response,
            mock_get_all_included_users_response_empty,
        ]

        py42.settings.items_per_page = 1
        for _ in watchlists_service.get_all_included_users(watchlist_id=WATCHLIST_ID):
            pass
        py42.settings.items_per_page = 500

        assert mock_connection.get.call_count == 3

    def test_add_included_users_by_watchlist_id_calls_post_with_expected_params(
        self, mock_connection
    ):
        watchlists_service = WatchlistsService(mock_connection)
        user_ids = ["user@email.com", "test@code42.com"]
        watchlists_service.add_included_users_by_watchlist_id(
            watchlist_id=WATCHLIST_ID, user_ids=user_ids
        )
        data = {"userIds": user_ids, "watchlistId": WATCHLIST_ID}
        mock_connection.post.assert_called_once_with(
            f"{URI}/{WATCHLIST_ID}/included-users/add", json=data
        )

    def test_add_included_users_by_watchlist_id_raises_py42_not_found_when_id_not_found(
        self, mock_connection, mock_watchlist_not_found_error
    ):
        watchlists_service = WatchlistsService(mock_connection)
        mock_connection.post.side_effect = mock_watchlist_not_found_error
        with pytest.raises(Py42WatchlistNotFound) as err:
            watchlists_service.add_included_users_by_watchlist_id(
                watchlist_id="invalid-id", user_ids=["user1", "user2"]
            )

        assert err.value.args[0] == "Watchlist ID 'invalid-id' not found."

    def test_add_included_users_by_watchlist_id_raises_py42_not_found_when_user_id_not_found(
        self, mock_connection, mock_user_not_found_error
    ):
        watchlists_service = WatchlistsService(mock_connection)
        mock_connection.post.side_effect = mock_user_not_found_error
        with pytest.raises(Py42NotFoundError) as err:
            watchlists_service.add_included_users_by_watchlist_id(
                watchlist_id="invalid-id", user_ids=["user1", "user2"]
            )

        assert err.value.args[0] == "User not found"

    def test_add_included_users_by_watchlist_type_calls_add_with_expected_params_when_watchlist_exists(
        self, mock_connection
    ):
        watchlists_service = WatchlistsService(mock_connection)
        user_ids = ["user@email.com", "test@code42.com"]

        # set watchlist dict
        watchlists_service._watchlist_type_id_map = {}
        watchlists_service.watchlist_type_id_map[WATCHLIST_TYPE] = WATCHLIST_ID

        watchlists_service.add_included_users_by_watchlist_type(
            user_ids, WATCHLIST_TYPE
        )
        data = {"userIds": user_ids, "watchlistId": WATCHLIST_ID}
        mock_connection.post.assert_called_once_with(
            f"{URI}/{WATCHLIST_ID}/included-users/add", json=data
        )

    def test_add_included_users_by_watchlist_type_creates_watchlist_and_calls_with_expected_params_when_watchlist_does_not_exist(
        self, mock_connection, mocker
    ):
        watchlists_service = WatchlistsService(mock_connection)
        user_ids = ["user@email.com", "test@code42.com"]
        watchlists_service._watchlist_type_id_map = {}

        # mock create call response
        requests_response = mocker.MagicMock(spec=Response)
        requests_response.text = json.dumps(WATCHLIST_RESPONSE)
        mock_connection.post.return_value = Py42Response(requests_response)

        watchlists_service.add_included_users_by_watchlist_type(
            user_ids, WATCHLIST_TYPE
        )

        assert (
            watchlists_service.watchlist_type_id_map["DEPARTING_EMPLOYEE"]
            == WATCHLIST_ID
        )
        data = {"userIds": user_ids, "watchlistId": WATCHLIST_ID}
        mock_connection.post.assert_called_with(
            f"{URI}/{WATCHLIST_ID}/included-users/add", json=data
        )

    def test_add_included_users_by_watchlist_type_raises_py42_not_found_when_user_id_not_found(
        self, mock_connection, mock_user_not_found_error
    ):
        watchlists_service = WatchlistsService(mock_connection)

        # set watchlist dict
        watchlists_service._watchlist_type_id_map = {}
        watchlists_service.watchlist_type_id_map[WATCHLIST_TYPE] = WATCHLIST_ID

        mock_connection.post.side_effect = mock_user_not_found_error
        with pytest.raises(Py42NotFoundError) as err:
            watchlists_service.add_included_users_by_watchlist_type(
                user_ids=["user1", "user2"], watchlist_type=WATCHLIST_TYPE
            )

        assert err.value.args[0] == "User not found"

    def test_delete_included_users_by_watchlist_id_calls_post_with_expected_params_and_updates_dict(
        self, mock_connection
    ):
        watchlists_service = WatchlistsService(mock_connection)
        user_ids = ["user@email.com", "test@code42.com"]
        watchlists_service.delete_included_users_by_watchlist_id(
            watchlist_id=WATCHLIST_ID, user_ids=user_ids
        )
        data = {"userIds": user_ids, "watchlistId": WATCHLIST_ID}
        mock_connection.post.assert_called_once_with(
            f"{URI}/{WATCHLIST_ID}/included-users/delete", json=data
        )

    def test_delete_included_users_by_watchlist_id_raises_py42_not_found_when_id_not_found(
        self, mock_connection, mock_watchlist_not_found_error
    ):
        watchlists_service = WatchlistsService(mock_connection)
        mock_connection.post.side_effect = mock_watchlist_not_found_error
        with pytest.raises(Py42WatchlistNotFound) as err:
            watchlists_service.delete_included_users_by_watchlist_id(
                watchlist_id="invalid-id", user_ids=["user1", "user2"]
            )

        assert err.value.args[0] == "Watchlist ID 'invalid-id' not found."

    def test_delete_included_users_by_watchlist_id_raises_py42_not_found_when_user_id_not_found(
        self, mock_connection, mock_user_not_found_error
    ):
        watchlists_service = WatchlistsService(mock_connection)
        mock_connection.post.side_effect = mock_user_not_found_error
        with pytest.raises(Py42NotFoundError) as err:
            watchlists_service.delete_included_users_by_watchlist_id(
                watchlist_id="invalid-id", user_ids=["user1", "user2"]
            )

        assert err.value.args[0] == "User not found"

    def test_delete_included_users_by_watchlist_type_calls_post_with_expected_params_when_watchlist_exists(
        self, mock_connection
    ):
        watchlists_service = WatchlistsService(mock_connection)
        user_ids = ["user@email.com", "test@code42.com"]

        # set watchlist dict
        watchlists_service._watchlist_type_id_map = {}
        watchlists_service.watchlist_type_id_map[WATCHLIST_TYPE] = WATCHLIST_ID

        watchlists_service.delete_included_users_by_watchlist_type(
            user_ids, WATCHLIST_TYPE
        )

        data = {"userIds": user_ids, "watchlistId": WATCHLIST_ID}
        mock_connection.post.assert_called_once_with(
            f"{URI}/{WATCHLIST_ID}/included-users/delete", json=data
        )

    def test_delete_included_users_by_watchlist_type_raises_error_when_watchlist_does_not_exist(
        self, mock_connection
    ):
        watchlists_service = WatchlistsService(mock_connection)
        user_ids = ["user@email.com", "test@code42.com"]

        with pytest.raises(Py42Error) as err:
            watchlists_service.delete_included_users_by_watchlist_type(
                user_ids, WATCHLIST_TYPE
            )

        assert (
            err.value.args[0] == f"Couldn't find watchlist of type:'{WATCHLIST_TYPE}'."
        )

    def test_delete_included_users_by_watchlist_type_raises_py42_not_found_when_user_id_not_found(
        self, mock_connection, mock_user_not_found_error
    ):
        watchlists_service = WatchlistsService(mock_connection)

        # set watchlist dict
        watchlists_service._watchlist_type_id_map = {}
        watchlists_service.watchlist_type_id_map[WATCHLIST_TYPE] = WATCHLIST_ID

        mock_connection.post.side_effect = mock_user_not_found_error
        with pytest.raises(Py42NotFoundError) as err:
            watchlists_service.delete_included_users_by_watchlist_type(
                user_ids=["user1", "user2"], watchlist_type=WATCHLIST_TYPE
            )

        assert err.value.args[0] == "User not found"

    def test_get_page_members_calls_get_with_expected_params(self, mock_connection):
        watchlists_service = WatchlistsService(mock_connection)
        watchlists_service.get_page_watchlist_members(WATCHLIST_ID)
        data = {
            "page": 1,
            "page_size": None,
        }
        mock_connection.get.assert_called_once_with(
            f"{URI}/{WATCHLIST_ID}/members", params=data
        )

    def test_get_page_members_calls_get_with_optional_params(self, mock_connection):
        watchlists_service = WatchlistsService(mock_connection)
        watchlists_service.get_page_watchlist_members(
            WATCHLIST_ID, page_num=1, page_size=10
        )
        data = {
            "page": 1,
            "page_size": 10,
        }
        mock_connection.get.assert_called_once_with(
            f"{URI}/{WATCHLIST_ID}/members", params=data
        )

    def test_get_all_members_calls_get_page_expected_number_of_times(
        self,
        mock_connection,
        mock_get_all_members_response,
        mock_get_all_members_response_empty,
    ):
        watchlists_service = WatchlistsService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_members_response,
            mock_get_all_members_response,
            mock_get_all_members_response_empty,
        ]

        py42.settings.items_per_page = 1
        for _ in watchlists_service.get_all_watchlist_members(WATCHLIST_ID):
            pass
        py42.settings.items_per_page = 500

        assert mock_connection.get.call_count == 3

    def test_get_watchlist_member_calls_get_with_expected_params(self, mock_connection):
        watchlists_service = WatchlistsService(mock_connection)
        watchlists_service.get_watchlist_member(WATCHLIST_ID, "user-42")
        mock_connection.get.assert_called_once_with(
            f"{URI}/{WATCHLIST_ID}/members/user-42"
        )

    def test_get_watchlist_member_raises_py42_not_found_when_id_not_found(
        self, mock_connection, mock_not_found_error
    ):
        watchlists_service = WatchlistsService(mock_connection)
        mock_connection.get.side_effect = mock_not_found_error
        with pytest.raises(Py42WatchlistOrUserNotFound) as err:
            watchlists_service.get_watchlist_member(
                "invalid-watchlist-id", "invalid-user-id"
            )

        assert (
            err.value.args[0]
            == "Watchlist ID 'invalid-watchlist-id' or User ID 'invalid-user-id' not found."
        )
