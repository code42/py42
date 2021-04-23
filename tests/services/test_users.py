# -*- coding: utf-8 -*-
import pytest
from requests import HTTPError
from requests import Response

import py42.settings
from py42.exceptions import Py42ActiveLegalHoldError
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42InternalServerError
from py42.exceptions import Py42OrgNotFoundError
from py42.exceptions import Py42UserAlreadyExistsError
from py42.exceptions import Py42UsernameMustBeEmailError
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
MOCK_GET_USER_RESPONSE = '{"totalCount": 3000, "users": ["foo"]}'
MOCK_EMPTY_GET_USER_RESPONSE = '{"totalCount": 3000, "users": []}'
MOCK_text = '{"item_list_key": [{"foo": "foo_val"}, {"bar": "bar_val"}]}'
MOCK_USER_DUPLICATE_ERROR_TEXT = '{"body": "USER_DUPLICATE"}'
MOCK_USERNAME_MUST_BE_EMAIL_TEXT = '{"data": [{"name": "USERNAME_NOT_AN_EMAIL"}]}'


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

    @pytest.fixture
    def put_api_mock_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_text
        return Py42Response(response)

    @pytest.fixture
    def internal_server_error(self, mocker):
        base_error = mocker.MagicMock(spec=HTTPError)
        base_error.response = mocker.MagicMock(spec=Response)
        return Py42InternalServerError(base_error)

    @pytest.fixture
    def post_user_duplicate_error_response(self, internal_server_error):
        internal_server_error.response.text = MOCK_USER_DUPLICATE_ERROR_TEXT
        return internal_server_error

    @pytest.fixture
    def post_username_must_be_email_error_response(self, internal_server_error):
        internal_server_error.response.text = MOCK_USERNAME_MUST_BE_EMAIL_TEXT
        return internal_server_error

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
            "orgUid": org_uid,
            "username": username,
            "email": username,
            "password": password,
            "firstName": name,
            "lastName": name,
            "notes": note,
        }

        mock_connection.post.assert_called_once_with(USER_URI, json=expected_params)

    def test_create_user_calls_post_and_returns_user_duplicate_error(
        self, mock_connection, post_user_duplicate_error_response
    ):
        user_service = UserService(mock_connection)
        mock_connection.post.side_effect = post_user_duplicate_error_response
        org_uid = "TEST_ORG_ID"
        username = "TEST_ORG@TEST.COM"
        password = "password"
        name = "TESTNAME"
        note = "Test Note"
        with pytest.raises(Py42UserAlreadyExistsError):
            user_service.create_user(
                org_uid, username, username, password, name, name, note
            )

    def test_create_user_when_get_unhandled_internal_server_error_raises_base_error(
        self, mock_connection, internal_server_error
    ):
        user_service = UserService(mock_connection)
        mock_connection.post.side_effect = internal_server_error
        with pytest.raises(Py42InternalServerError):
            user_service.create_user("123", "123@example.com", "123@example.com")

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

    def test_get_page_when_org_not_found_raises_expected_error(
        self, mocker, mock_connection
    ):
        def side_effect(*args, **kwargs):
            base_err = mocker.MagicMock(spec=HTTPError)
            base_err.response = mocker.MagicMock(spec=Response)
            base_err.response.text = (
                '[{"name":"SYSTEM","description":"Organization was not found"}]'
            )
            raise Py42BadRequestError(base_err)

        mock_connection.get.side_effect = side_effect
        service = UserService(mock_connection)

        with pytest.raises(Py42OrgNotFoundError) as err:
            service.get_page(1, org_uid="TestOrgUid")

        assert str(err.value) == "The organization with UID 'TestOrgUid' was not found."

    def test_get_page_when_bad_request_raises(self, mocker, mock_connection):
        def side_effect(*args, **kwargs):
            base_err = mocker.MagicMock(spec=HTTPError)
            base_err.response = mocker.MagicMock(spec=Response)
            base_err.response.text = "BAD REQUEST"
            raise Py42BadRequestError(base_err)

        mock_connection.get.side_effect = side_effect
        service = UserService(mock_connection)

        with pytest.raises(Py42BadRequestError):
            service.get_page(1, org_uid="TestOrgUid")

    def test_deactivate_when_user_in_legal_hold_raises_active_legal_hold_error(
        self, mocker, mock_connection
    ):
        def side_effect(url, json):
            if "UserDeactivation" in url:
                base_err = mocker.MagicMock(spec=HTTPError)
                base_err.response = mocker.MagicMock(spec=Response)
                base_err.response.text = "ACTIVE_LEGAL_HOLD"
                raise Py42BadRequestError(base_err)

        mock_connection.put.side_effect = side_effect
        client = UserService(mock_connection)
        with pytest.raises(Py42ActiveLegalHoldError) as err:
            client.deactivate(1234)

        expected = "Cannot deactivate the user with ID 1234 as the user is involved in a legal hold matter."
        assert str(err.value) == expected

    def test_update_user_calls_put_with_expected_url_and_params(
        self, mock_connection, put_api_mock_response
    ):
        user_service = UserService(mock_connection)
        mock_connection.post.return_value = put_api_mock_response
        user_id = "TEST_USER_ID"
        expected_uri = "{}/{}?idType=uid".format(USER_URI, user_id)
        username = "TEST_ORG@TEST.COM"
        email = "TEST_EMAIL@TEST.com"
        password = "password"
        first_name = "FIRSTNAME"
        last_name = "LASTNAME"
        note = "Test Note"
        quota = 12345
        user_service.update_user(
            user_id,
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
            notes=note,
            archive_size_quota_bytes=quota,
        )
        expected_params = {
            "username": username,
            "email": email,
            "password": password,
            "firstName": first_name,
            "lastName": last_name,
            "notes": note,
            "quotaInBytes": quota,
        }
        mock_connection.put.assert_called_once_with(expected_uri, json=expected_params)

    def test_update_user_does_not_include_empty_params(
        self, mock_connection, put_api_mock_response
    ):
        user_service = UserService(mock_connection)
        mock_connection.post.return_value = put_api_mock_response
        user_id = "TEST_USER_ID"
        expected_uri = "{}/{}?idType=uid".format(USER_URI, user_id)
        username = "TEST_ORG@TEST.COM"
        user_service.update_user(user_id, username=username)
        expected_params = {
            "username": username,
            "email": None,
            "password": None,
            "firstName": None,
            "lastName": None,
            "notes": None,
            "quotaInBytes": None,
        }
        mock_connection.put.assert_called_once_with(expected_uri, json=expected_params)

    def test_update_user_when_get_internal_server_error_containing_must_be_email_text_raises_expected_error(
        self, mock_connection, post_username_must_be_email_error_response
    ):
        user_service = UserService(mock_connection)
        mock_connection.put.side_effect = post_username_must_be_email_error_response
        with pytest.raises(Py42UsernameMustBeEmailError):
            user_service.update_user("123", username="foo")

    def test_update_user_when_get_unhandled_internal_server_error_raises_base_error(
        self, mock_connection, internal_server_error
    ):
        user_service = UserService(mock_connection)
        mock_connection.put.side_effect = internal_server_error
        with pytest.raises(Py42InternalServerError):
            user_service.update_user("123", username="foo")
