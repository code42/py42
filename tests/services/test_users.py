# -*- coding: utf-8 -*-
import pytest
from requests import Response

import py42.settings
from py42.exceptions import Py42UserDoesNotExistError
from py42.response import Py42Response
from py42.services.users import UserService

USER_URI = "/api/User"

DEFAULT_GET_ALL_PARAMS = {
    "active": None,
    "email": None,
    "orgUid": None,
    "roleId": None,
    "pgNum": 1,
    "pgSize": 500,
    "q": None,
}

MOCK_GET_USER_RESPONSE = """{"totalCount": 3000, "users": ["foo"]}"""

MOCK_EMPTY_GET_USER_RESPONSE = """{"totalCount": 3000, "users": []}"""

MOCK_text = '{"item_list_key": [{"foo": "foo_val"}, {"bar": "bar_val"}]}'


class TestUserService(object):
    @pytest.fixture
    def mock_get_users_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_GET_USER_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_users_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_EMPTY_GET_USER_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def post_api_mock_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_text
        return Py42Response(response)

    def test_create_user_calls_post_with_expected_url_and_params(
        self, mock_connection, post_api_mock_response
    ):
        user_service = UserService(mock_connection)
        mock_connection.post.return_value = post_api_mock_response
        org_uid = "TEST_ORG_ID"
        username = "TEST_ORG@TEST.COM"
        password = "password"
        name = "TESTNAME"
        note = "Test Note"
        user_service.create_user(
            org_uid, username, username, password, name, name, note
        )
        expected_params = {
            u"orgUid": org_uid,
            u"username": username,
            u"email": username,
            u"password": password,
            u"firstName": name,
            u"lastName": name,
            u"notes": note,
        }

        mock_connection.post.assert_called_once_with(USER_URI, json=expected_params)

    def test_get_all_calls_get_with_uri_and_params(
        self, mock_connection, mock_get_users_response
    ):
        mock_connection.get.side_effect = [mock_get_users_response]
        service = UserService(mock_connection)
        for _ in service.get_all():
            break
        first_call = mock_connection.get.call_args_list[0]
        assert first_call[0][0] == USER_URI
        assert first_call[1]["params"] == DEFAULT_GET_ALL_PARAMS

    def test_unicode_username_get_user_by_username_calls_get_with_username(
        self, mock_connection, mock_get_users_response
    ):
        username = u"您已经发现了秘密信息"
        mock_connection.get.return_value = mock_get_users_response
        service = UserService(mock_connection)
        service.get_by_username(username)
        expected_params = {u"username": username}
        mock_connection.get.assert_called_once_with(USER_URI, params=expected_params)

    def test_get_by_username_when_empty_list_returns_raises_user_not_exists(
        self, mock_connection, mock_get_users_empty_response
    ):
        mock_connection.get.return_value = mock_get_users_empty_response
        service = UserService(mock_connection)
        with pytest.raises(Py42UserDoesNotExistError) as err:
            service.get_by_username("username")

        assert str(err.value) == "User 'username' does not exist."

    def test_get_user_by_id_calls_get_with_uri_and_params(
        self, mock_connection, successful_response
    ):
        mock_connection.get.return_value = successful_response
        service = UserService(mock_connection)
        service.get_by_id(123456)
        uri = "{}/{}".format(USER_URI, 123456)
        mock_connection.get.assert_called_once_with(uri, params={})

    def test_get_all_calls_get_expected_number_of_times(
        self, mock_connection, mock_get_users_response, mock_get_users_empty_response
    ):
        py42.settings.items_per_page = 1
        service = UserService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_users_response,
            mock_get_users_response,
            mock_get_users_empty_response,
        ]
        for _ in service.get_all():
            pass
        py42.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_scim_data_by_uid_calls_get_with_expected_uri_and_params(
        self, mock_connection
    ):
        service = UserService(mock_connection)
        service.get_scim_data_by_uid("USER_ID")
        uri = "/api/v7/scim-user-data/collated-view"
        mock_connection.get.assert_called_once_with(uri, params={"userId": "USER_ID"})

    def test_get_available_roles_calls_get_with_expected_uri(self, mock_connection):
        service = UserService(mock_connection)
        service.get_available_roles()
        uri = "/api/v4/role/view"
        mock_connection.get.assert_called_once_with(uri)

    def test_get_roles_calls_get_with_expected_uri(self, mock_connection):
        service = UserService(mock_connection)
        service.get_roles(12345)
        uri = "/api/UserRole/12345"
        mock_connection.get.assert_called_once_with(uri)

    def test_add_role_calls_post_with_expected_uri_and_data(self, mock_connection):
        service = UserService(mock_connection)
        service.add_role(12345, "Test Role Name")
        uri = "/api/UserRole"
        assert mock_connection.post.call_args[0][0] == uri
        assert mock_connection.post.call_args[1]["json"]["roleName"] == "Test Role Name"
        assert mock_connection.post.call_args[1]["json"]["userId"] == 12345

    def test_delete_role_calls_delete_with_expected_uri_and_params(
        self, mock_connection
    ):
        service = UserService(mock_connection)
        service.remove_role(12345, "Test Role Name")
        uri = "/api/UserRole?userId=12345&roleName=Test%20Role%20Name"
        mock_connection.delete.assert_called_once_with(uri)

    def test_get_page_calls_get_with_expected_url_and_params(self, mock_connection):
        service = UserService(mock_connection)
        service.get_page(10, True, "email", "org", "role", 100, "q")
        mock_connection.get.assert_called_once_with(
            "/api/User",
            params={
                "active": True,
                "email": "email",
                "orgUid": "org",
                "roleId": "role",
                "pgNum": 10,
                "pgSize": 100,
                "q": "q",
            },
        )
