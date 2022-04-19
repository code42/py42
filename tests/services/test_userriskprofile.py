import json
from datetime import date
from datetime import datetime

import pytest
from requests import Response
from tests.conftest import create_mock_error
from tests.conftest import create_mock_response

import py42.settings
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42NotFoundError
from py42.response import Py42Response
from py42.services.userriskprofile import UserRiskProfileService

USER_ID = "user-42"
USERNAME = "risk-user@code42.com"
GET_ALL_RESPONSE = '{"userRiskProfiles":["test"], "totalCount":1}'
GET_ALL_RESPONSE_EMPTY = '{"userRiskProfiles": [], "totalCount":0}'
GET_ALL_RESPONSE_POPULATED = {
    "userRiskProfiles": [{"username": "risk-user@code42.com", "userId": "user-42"}],
    "totalCount": 1,
}
CLOUD_ALIASES = ["test@code42.com", "user1@email.com"]


URI = "/v1/user-risk-profiles"


@pytest.fixture
def mock_get_all_response(mocker):
    return create_mock_response(mocker, GET_ALL_RESPONSE)


@pytest.fixture
def mock_get_all_response_empty(mocker):
    return create_mock_response(mocker, GET_ALL_RESPONSE_EMPTY)


@pytest.fixture
def mock_not_found_error(mocker):
    return create_mock_error(Py42NotFoundError, mocker, "Not Found Error Msg")


class TestUserRiskProfileService:
    def test_get_by_id_calls_get_with_expected_params(self, mock_connection):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        user_risk_profile_service.get_by_id(USER_ID)
        mock_connection.get.assert_called_once_with(f"{URI}/{USER_ID}")

    def test_get_by_id_raises_py42_not_found_when_id_not_found(
        self, mock_connection, mock_not_found_error
    ):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        mock_connection.get.side_effect = mock_not_found_error
        with pytest.raises(Py42NotFoundError) as err:
            user_risk_profile_service.get_by_id("fake-id")

        assert (
            err.value.args[0]
            == "User risk profile for user with the ID 'fake-id' not found."
        )

    def test_get_by_username_calls_get_with_expected_params(
        self, mock_connection, mocker
    ):
        requests_response = mocker.MagicMock(spec=Response)
        requests_response.text = json.dumps(GET_ALL_RESPONSE_POPULATED)
        py42_response = Py42Response(requests_response)
        mock_connection.get.return_value = py42_response

        user_risk_profile_service = UserRiskProfileService(mock_connection)
        user_risk_profile_service.get_by_username(USERNAME)
        mock_connection.get.assert_called_with(f"{URI}/{USER_ID}")

    def test_update_calls_patch_with_expected_params_when_all_fields_provided(
        self, mock_connection
    ):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        paths = ["startDate", "endDate", "notes"]
        user_risk_profile_service.update(
            USER_ID,
            start_date="2010-07-01",
            end_date="2022-01-04",
            notes="this is a test note.",
        )
        params = {"paths": ", ".join(paths)}
        data = {
            "endDate": {"day": 4, "month": 1, "year": 2022},
            "notes": "this is a test note.",
            "startDate": {"day": 1, "month": 7, "year": 2010},
        }
        mock_connection.patch.assert_called_once_with(
            f"{URI}/{USER_ID}", json=data, params=params
        )

    def test_update_calls_patch_with_expected_params_when_datetime_provided(
        self, mock_connection
    ):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        paths = ["startDate", "endDate", "notes"]
        user_risk_profile_service.update(
            USER_ID,
            start_date=date(2010, 7, 1),
            end_date=datetime(2022, 1, 4),
            notes="this is a test note.",
        )
        params = {"paths": ", ".join(paths)}
        data = {
            "endDate": {"day": 4, "month": 1, "year": 2022},
            "notes": "this is a test note.",
            "startDate": {"day": 1, "month": 7, "year": 2010},
        }
        mock_connection.patch.assert_called_once_with(
            f"{URI}/{USER_ID}", json=data, params=params
        )

    def test_update_calls_patch_with_expected_params_when_empty_strings_provided(
        self, mock_connection
    ):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        paths = ["startDate", "endDate", "notes"]
        user_risk_profile_service.update(USER_ID, end_date="", start_date="", notes="")
        params = {"paths": ", ".join(paths)}
        data = {
            "endDate": {"day": None, "month": None, "year": None},
            "notes": None,
            "startDate": {"day": None, "month": None, "year": None},
        }
        mock_connection.patch.assert_called_once_with(
            f"{URI}/{USER_ID}", json=data, params=params
        )

    def test_get_page_calls_get_with_expected_params(self, mock_connection):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        user_risk_profile_service.get_page(page_num=1, page_size=10)
        data = {
            "page": 1,
            "page_size": 10,
            "manager_id": None,
            "title": None,
            "division": None,
            "department": None,
            "employment_type": None,
            "country": None,
            "region": None,
            "locality": None,
            "active": None,
            "deleted": None,
            "support_user": None,
        }
        mock_connection.get.assert_called_once_with(URI, params=data)

    def test_get_page_calls_get_with_optional_params(self, mock_connection):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        user_risk_profile_service.get_page(
            page_num=1,
            page_size=10,
            manager_id="manager-1",
            title="engineer",
            division="division",
            department="engineering",
            employment_type="full-time",
            country="usa",
            region="midwest",
            locality="local",
            active=True,
            deleted=False,
            support_user=False,
        )
        data = {
            "page": 1,
            "page_size": 10,
            "manager_id": "manager-1",
            "title": "engineer",
            "division": "division",
            "department": "engineering",
            "employment_type": "full-time",
            "country": "usa",
            "region": "midwest",
            "locality": "local",
            "active": True,
            "deleted": False,
            "support_user": False,
        }
        mock_connection.get.assert_called_once_with(URI, params=data)

    def test_get_all_calls_get_expected_number_of_times(
        self, mock_connection, mock_get_all_response, mock_get_all_response_empty
    ):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_response,
            mock_get_all_response,
            mock_get_all_response_empty,
        ]

        py42.settings.items_per_page = 1
        for _ in user_risk_profile_service.get_all():
            pass

        py42.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_all_calls_get_with_expected_uri_and_params(
        self, mock_connection, mock_get_all_response_empty
    ):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        mock_connection.get.side_effect = [mock_get_all_response_empty]

        for _ in user_risk_profile_service.get_all(
            manager_id="manager-1",
            title="engineer",
            division="division",
            department="engineering",
            employment_type="full-time",
            country="usa",
            region="midwest",
            locality="local",
            active=True,
            deleted=False,
            support_user=False,
        ):
            pass

        data = {
            "page": 1,
            "page_size": 500,
            "manager_id": "manager-1",
            "title": "engineer",
            "division": "division",
            "department": "engineering",
            "employment_type": "full-time",
            "country": "usa",
            "region": "midwest",
            "locality": "local",
            "active": True,
            "deleted": False,
            "support_user": False,
        }
        mock_connection.get.assert_called_once_with(URI, params=data)

    def test_add_cloud_aliases_calls_post_with_expected_params(self, mock_connection):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        user_risk_profile_service.add_cloud_aliases(USER_ID, CLOUD_ALIASES)
        data = {"cloudAliases": CLOUD_ALIASES, "userId": USER_ID}
        mock_connection.post.assert_called_once_with(
            f"{URI}/{USER_ID}/add-cloud-aliases", json=data
        )

    def test_add_cloud_aliases_raises_py42_error_when_id_not_found(
        self, mock_connection, mock_not_found_error
    ):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        mock_connection.post.side_effect = mock_not_found_error
        with pytest.raises(Py42NotFoundError) as err:
            user_risk_profile_service.add_cloud_aliases("fake-id", "cloud-alias")

        assert (
            err.value.args[0]
            == "User risk profile for user with the ID 'fake-id' not found."
        )

    def test_add_cloud_aliases_raises_py42_error_when_alias_limit_reached(
        self, mock_connection, mocker
    ):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        mock_alias_limit_error = create_mock_error(
            Py42BadRequestError,
            mocker,
            "Cloud usernames must be less than or equal to 2",
        )
        mock_connection.post.side_effect = mock_alias_limit_error
        with pytest.raises(Py42BadRequestError) as err:
            user_risk_profile_service.add_cloud_aliases(
                "fake-id", ["too", "many", "aliases"]
            )

        assert (
            err.value.args[0]
            == "Cloud alias limit exceeded. A max of 2 cloud aliases are allowed."
        )

    def test_delete_cloud_aliases_calls_post_with_expected_params(
        self, mock_connection
    ):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        user_risk_profile_service.delete_cloud_aliases(USER_ID, CLOUD_ALIASES)
        data = {"cloudAliases": CLOUD_ALIASES, "userId": USER_ID}
        mock_connection.post.assert_called_once_with(
            f"{URI}/{USER_ID}/delete-cloud-aliases", json=data
        )

    def test_delete_cloud_aliases_raises_py42_error_when_id_not_found(
        self, mock_connection, mock_not_found_error
    ):
        user_risk_profile_service = UserRiskProfileService(mock_connection)
        mock_connection.post.side_effect = mock_not_found_error
        with pytest.raises(Py42NotFoundError) as err:
            user_risk_profile_service.delete_cloud_aliases("fake-id", "cloud-alias")

        assert (
            err.value.args[0]
            == "User risk profile for user with the ID 'fake-id' not found."
        )
