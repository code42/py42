import json
from unittest.mock import patch

import pytest
from tests.conftest import create_mock_error
from tests.conftest import create_mock_response

import pycpg.settings
from pycpg.exceptions import PycpgActiveLegalHoldError
from pycpg.exceptions import PycpgBadRequestError
from pycpg.exceptions import PycpgInternalServerError
from pycpg.exceptions import PycpgInvalidEmailError
from pycpg.exceptions import PycpgInvalidPasswordError
from pycpg.exceptions import PycpgInvalidUsernameError
from pycpg.exceptions import PycpgNotFoundError
from pycpg.exceptions import PycpgOrgNotFoundError
from pycpg.exceptions import PycpgUserAlreadyExistsError
from pycpg.exceptions import PycpgUsernameMustBeEmailError
from pycpg.services.users import UserService

USER_URI = "/api/v1/User"
USER_URI_V3 = "/api/v3/users"
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
MOCK_TEXT = '{"item_list_key": [{"foo": "foo_val"}, {"bar": "bar_val"}]}'
MOCK_USER_DUPLICATE_ERROR_TEXT = '{"body": "USER_DUPLICATE"}'
MOCK_USERNAME_MUST_BE_EMAIL_TEXT = '{"data": [{"name": "USERNAME_NOT_AN_EMAIL"}]}'
MOCK_INVALID_EMAIL_TEXT = '{"data": [{"name": "EMAIL_INVALID"}]}'
MOCK_INVALID_PASSWORD_TEXT = '{"data": [{"name": "NEW_PASSWORD_INVALID"}]}'
MOCK_INVALID_USERNAME_TEXT = '{"data": [{"name": "INVALID_USERNAME"}]}'
TEST_USER_UID = "1004210042"
MOCK_ROLE_IDS = ["desktop-user", "proe-user", "customer-cloud-admin"]
MOCK_GET_USER_BY_ID_RESPONSE = {
    "data": {
        "userId": 12345,
        "userUid": TEST_USER_UID,
        "status": "Active",
        "username": "test@crashPlan.com",
        "email": "test@crashPlan.com",
        "firstName": "test",
        "lastName": "mctest",
    }
}
MOCK_ROLES_LIST = [
    {
        "roleId": "desktop-user",
        "roleName": "Desktop User",
        "modificationDate": "2022-01-14T17:30:29.227+00:00",
        "creationDate": "2019-01-10T20:29:51.343+00:00",
        "permissionIds": [],
    },
    {
        "roleId": "proe-user",
        "roleName": "PROe User",
        "modificationDate": "2022-01-14T17:30:29.098+00:00",
        "creationDate": "2019-01-10T20:29:51.607+00:00",
        "permissionIds": [],
    },
    {
        "roleId": "customer-cloud-admin",
        "roleName": "Customer Cloud Admin",
        "modificationDate": "2022-05-06T18:11:21.780+00:00",
        "creationDate": "2019-01-10T20:29:51.330+00:00",
        "permissionIds": [],
    },
]
MOCK_GET_ROLES_RESPONSE = {"data": MOCK_ROLES_LIST}
MOCK_ALL_ROLES_LIST = MOCK_ROLES_LIST.copy()
MOCK_ALL_ROLES_LIST.append(
    {
        "roleId": "alert-emails",
        "roleName": "Alert Emails",
        "numberOfUsers": 1,
        "creationDate": "2019-01-10T20:29:51.241Z",
        "modificationDate": "2021-02-03T21:12:20.660Z",
        "permissions": [
            {
                "permission": "admin.receives_alert.email",
                "description": "Receives automated backup reports and alerts by email",
            }
        ],
    }
)

MOCK_GET_AVAILABLE_ROLES_RESPONSE = {"data": MOCK_ALL_ROLES_LIST}


class TestUserService:
    @pytest.fixture
    def mock_get_available_roles_response(self, mocker):
        return create_mock_response(
            mocker, json.dumps(MOCK_GET_AVAILABLE_ROLES_RESPONSE)
        )

    @pytest.fixture
    def mock_get_user_by_id_response(self, mocker):
        return create_mock_response(mocker, json.dumps(MOCK_GET_USER_BY_ID_RESPONSE))

    @pytest.fixture
    def mock_get_roles_response(self, mocker):
        return create_mock_response(mocker, json.dumps(MOCK_GET_ROLES_RESPONSE))

    @pytest.fixture
    def mock_get_users_response(self, mocker):
        return create_mock_response(mocker, MOCK_GET_USER_RESPONSE)

    @pytest.fixture
    def mock_get_users_empty_response(self, mocker):
        return create_mock_response(mocker, MOCK_EMPTY_GET_USER_RESPONSE)

    @pytest.fixture
    def post_api_mock_response(self, mocker):
        return create_mock_response(mocker, MOCK_TEXT)

    @pytest.fixture
    def put_api_mock_response(self, mocker):
        return create_mock_response(mocker, MOCK_TEXT)

    @pytest.fixture
    def internal_server_error(self, mocker):
        return create_mock_error(PycpgInternalServerError, mocker, "")

    @pytest.fixture
    def user_duplicate_error_response(self, mocker):
        return create_mock_error(
            PycpgInternalServerError, mocker, MOCK_USER_DUPLICATE_ERROR_TEXT
        )

    @pytest.fixture
    def username_must_be_email_error_response(self, mocker):
        return create_mock_error(
            PycpgInternalServerError, mocker, MOCK_USERNAME_MUST_BE_EMAIL_TEXT
        )

    @pytest.fixture
    def invalid_email_error_response(self, mocker):
        return create_mock_error(
            PycpgInternalServerError, mocker, MOCK_INVALID_EMAIL_TEXT
        )

    @pytest.fixture
    def invalid_password_error_response(self, mocker):
        return create_mock_error(
            PycpgInternalServerError, mocker, MOCK_INVALID_PASSWORD_TEXT
        )

    @pytest.fixture
    def invalid_username_error_response(self, mocker):
        return create_mock_error(
            PycpgInternalServerError, mocker, MOCK_INVALID_USERNAME_TEXT
        )

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
        self, mock_connection, user_duplicate_error_response
    ):
        user_service = UserService(mock_connection)
        mock_connection.post.side_effect = user_duplicate_error_response
        org_uid = "TEST_ORG_ID"
        username = "TEST_ORG@TEST.COM"
        password = "password"
        name = "TESTNAME"
        note = "Test Note"
        with pytest.raises(PycpgUserAlreadyExistsError):
            user_service.create_user(
                org_uid, username, username, password, name, name, note
            )

    def test_create_user_when_get_unhandled_internal_server_error_raises_base_error(
        self, mock_connection, internal_server_error
    ):
        user_service = UserService(mock_connection)
        mock_connection.post.side_effect = internal_server_error
        with pytest.raises(PycpgInternalServerError):
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
        username = "您已经发现了秘密信息"
        mock_connection.get.return_value = mock_get_users_response
        service = UserService(mock_connection)
        service.get_by_username(username)
        expected_params = {"username": username}
        mock_connection.get.assert_called_once_with(USER_URI, params=expected_params)

    def test_get_user_by_id_calls_get_with_uri_and_params(
        self, mock_connection, successful_response
    ):
        mock_connection.get.return_value = successful_response
        service = UserService(mock_connection)
        service.get_by_id(123456)
        uri = f"{USER_URI}/123456"
        mock_connection.get.assert_called_once_with(uri, params={})

    def test_get_all_calls_get_expected_number_of_times(
        self, mock_connection, mock_get_users_response, mock_get_users_empty_response
    ):
        pycpg.settings.items_per_page = 1
        service = UserService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_users_response,
            mock_get_users_response,
            mock_get_users_empty_response,
        ]
        for _ in service.get_all():
            pass
        pycpg.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_scim_data_by_uid_calls_get_with_expected_uri_and_params(
        self, mock_connection
    ):
        service = UserService(mock_connection)
        service.get_scim_data_by_uid("USER_ID")
        uri = "/api/v18/scim-user-data/collated-view"
        mock_connection.get.assert_called_once_with(uri, params={"userId": "USER_ID"})

    def test_get_available_roles_calls_get_with_expected_uri(self, mock_connection):
        service = UserService(mock_connection)
        service.get_available_roles()
        uri = "/api/v1/role"
        mock_connection.get.assert_called_once_with(uri)

    @patch.object(
        pycpg.services.users.UserService,
        "_get_user_uid_by_id",
        return_value=TEST_USER_UID,
    )
    def test_get_roles_calls_get_with_expected_uri(self, mock_connection):
        user_id = 12345
        service = UserService(mock_connection)
        service.get_roles(user_id)
        uri = f"{USER_URI_V3}/{TEST_USER_UID}/roles"
        mock_connection.get.assert_called_with(uri)

    def test_get_role_ids_calls_get_roles_and_returns_role_ids(
        self, mock_connection, mock_get_roles_response
    ):
        user_id = 12345

        with patch.object(
            pycpg.services.users.UserService,
            "get_roles",
            return_value=mock_get_roles_response,
        ) as mock_get_roles:
            service = UserService(mock_connection)
            role_ids = service._get_role_ids(user_id)

        mock_get_roles.assert_called_once_with(user_id)
        assert role_ids == ["desktop-user", "proe-user", "customer-cloud-admin"]

    @patch.object(
        pycpg.services.users.UserService,
        "_get_user_uid_by_id",
        return_value=TEST_USER_UID,
    )
    def test_update_roles_calls_put_with_expected_uri(self, mock_connection):
        service = UserService(mock_connection)
        role_ids = ["role-1", "role.name.2"]
        service._update_roles(12345, role_ids)
        uri = f"/api/v3/users/{TEST_USER_UID}/roles"
        data = {"roleIds": role_ids}
        mock_connection.put.assert_called_once_with(uri, json=data)

    def test_update_role_ids_calls_get_available_roles_and_returns_role_ids_when_add(
        self, mock_connection, mock_get_available_roles_response
    ):
        mock_connection.get.return_value = mock_get_available_roles_response
        service = UserService(mock_connection)
        role_ids = ["desktop-user", "proe-user", "customer-cloud-admin"]
        role_name = "Alert Emails"
        updated_role_ids = service._update_role_ids(role_name, role_ids, add=True)
        mock_connection.get.assert_called_once_with("/api/v1/role")
        assert updated_role_ids == [
            "desktop-user",
            "proe-user",
            "customer-cloud-admin",
            "alert-emails",
        ]

    def test_update_role_ids_calls_get_available_roles_and_returns_role_ids_when_remove(
        self, mock_connection, mock_get_available_roles_response
    ):
        mock_connection.get.return_value = mock_get_available_roles_response
        service = UserService(mock_connection)
        role_ids = ["desktop-user", "proe-user", "customer-cloud-admin"]
        role_name = "Desktop User"
        updated_role_ids = service._update_role_ids(role_name, role_ids, add=False)
        mock_connection.get.assert_called_once_with("/api/v1/role")
        assert updated_role_ids == [
            "proe-user",
            "customer-cloud-admin",
        ]

    def test_update_role_ids_calls_get_available_roles_and_returns_role_ids_when_and_given_role_id(
        self, mock_connection, mock_get_available_roles_response
    ):
        mock_connection.get.return_value = mock_get_available_roles_response
        service = UserService(mock_connection)
        role_ids = ["desktop-user", "proe-user", "customer-cloud-admin"]
        role_name = "alert-emails"
        updated_role_ids = service._update_role_ids(role_name, role_ids, add=True)
        mock_connection.get.assert_called_once_with("/api/v1/role")
        assert updated_role_ids == [
            "desktop-user",
            "proe-user",
            "customer-cloud-admin",
            "alert-emails",
        ]

    def test_update_role_ids_calls_get_available_roles_and_returns_role_ids_when_remove_and_given_role_id(
        self, mock_connection, mock_get_available_roles_response
    ):
        mock_connection.get.return_value = mock_get_available_roles_response
        service = UserService(mock_connection)
        role_ids = ["desktop-user", "proe-user", "customer-cloud-admin"]
        role_name = "desktop-user"
        updated_role_ids = service._update_role_ids(role_name, role_ids, add=False)
        mock_connection.get.assert_called_once_with("/api/v1/role")
        assert updated_role_ids == [
            "proe-user",
            "customer-cloud-admin",
        ]

    def test_get_page_calls_get_with_expected_url_and_params(self, mock_connection):
        service = UserService(mock_connection)
        service.get_page(10, True, "email", "org", "role", 100, "q")
        mock_connection.get.assert_called_once_with(
            "/api/v1/User",
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
        text = '[{"name":"SYSTEM","description":"Organization was not found"}]'
        mock_connection.get.side_effect = create_mock_error(
            PycpgBadRequestError, mocker, text
        )
        service = UserService(mock_connection)

        with pytest.raises(PycpgOrgNotFoundError) as err:
            service.get_page(1, org_uid="TestOrgUid")

        assert "The organization with UID 'TestOrgUid' was not found." in str(err.value)
        assert err.value.org_uid == "TestOrgUid"

    def test_get_page_when_bad_request_raises(self, mocker, mock_connection):
        mock_connection.get.side_effect = create_mock_error(
            PycpgBadRequestError, mocker, "BAD REQUEST"
        )
        service = UserService(mock_connection)

        with pytest.raises(PycpgBadRequestError):
            service.get_page(1, org_uid="TestOrgUid")

    def test_deactivate_when_user_in_legal_hold_raises_active_legal_hold_error(
        self, mocker, mock_connection
    ):
        mock_connection.post.side_effect = create_mock_error(
            PycpgBadRequestError, mocker, "ACTIVE_LEGAL_HOLD"
        )
        client = UserService(mock_connection)
        with pytest.raises(PycpgActiveLegalHoldError) as err:
            client.deactivate(1234)

        expected = (
            "Cannot deactivate the user with ID 1234 as the user is involved in "
            "a legal hold matter."
        )
        assert expected in str(err.value)
        assert err.value.resource == "user"
        assert err.value.resource_id == 1234

    def test_update_user_calls_put_with_expected_url_and_params(
        self, mock_connection, put_api_mock_response
    ):
        user_service = UserService(mock_connection)
        mock_connection.post.return_value = put_api_mock_response
        user_id = "TEST_USER_ID"
        expected_uri = f"{USER_URI}/{user_id}?idType=uid"
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
        expected_uri = f"{USER_URI}/{user_id}?idType=uid"
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

    def test_update_user_when_get_internal_server_error_containing_username_must_be_email_text_raises_expected_error(
        self, mock_connection, username_must_be_email_error_response
    ):
        user_service = UserService(mock_connection)
        mock_connection.put.side_effect = username_must_be_email_error_response
        with pytest.raises(PycpgUsernameMustBeEmailError) as err:
            user_service.update_user("123", username="foo")

        assert str(err.value) == "Username must be an email address."

    def test_update_user_when_get_internal_server_error_containing_email_invalid_raises_expected_error(
        self, mock_connection, invalid_email_error_response
    ):
        user_service = UserService(mock_connection)
        mock_connection.put.side_effect = invalid_email_error_response
        with pytest.raises(PycpgInvalidEmailError) as err:
            user_service.update_user("123", username="foo", email="test")

        assert "'test' is not a valid email." in str(err.value)
        assert err.value.email == "test"

    def test_update_user_when_get_internal_server_error_containing_password_invalid_raises_expected_error(
        self, mock_connection, invalid_password_error_response
    ):
        user_service = UserService(mock_connection)
        mock_connection.put.side_effect = invalid_password_error_response
        with pytest.raises(PycpgInvalidPasswordError) as err:
            user_service.update_user("123", username="foo", password="test")

        assert str(err.value) == "Invalid password."

    def test_update_user_when_get_internal_server_error_containing_username_invalid_raises_expected_error(
        self, mock_connection, invalid_username_error_response
    ):
        user_service = UserService(mock_connection)
        mock_connection.put.side_effect = invalid_username_error_response
        with pytest.raises(PycpgInvalidUsernameError) as err:
            user_service.update_user("123", username="foo")

        assert str(err.value) == "Invalid username."

    def test_update_user_when_get_unhandled_internal_server_error_raises_base_error(
        self, mock_connection, internal_server_error
    ):
        user_service = UserService(mock_connection)
        mock_connection.put.side_effect = internal_server_error
        with pytest.raises(PycpgInternalServerError):
            user_service.update_user("123", username="foo")

    @patch.object(
        pycpg.services.users.UserService,
        "_get_user_uid_by_id",
        return_value=TEST_USER_UID,
    )
    def test_block_calls_post_with_expected_uri(self, mock_connection):
        service = UserService(mock_connection)
        user_id = 12345
        service.block(user_id)
        uri = f"{USER_URI_V3}/{TEST_USER_UID}/block"
        mock_connection.post.assert_called_once_with(uri)

    @patch.object(
        pycpg.services.users.UserService,
        "_get_user_uid_by_id",
        return_value=TEST_USER_UID,
    )
    def test_unblock_calls_post_with_expected_uri(self, mock_connection):
        service = UserService(mock_connection)
        user_id = 12345
        service.unblock(user_id)
        uri = f"{USER_URI_V3}/{TEST_USER_UID}/unblock"
        mock_connection.post.assert_called_once_with(uri)

    @patch.object(
        pycpg.services.users.UserService,
        "_get_user_uid_by_id",
        return_value=TEST_USER_UID,
    )
    def test_deactivate_calls_post_with_expected_url_and_params(self, mock_connection):
        service = UserService(mock_connection)
        user_id = 12345
        service.deactivate(user_id, block_user=True)
        uri = f"{USER_URI_V3}/{TEST_USER_UID}/deactivate"
        data = {"block": True}
        mock_connection.post.assert_called_once_with(uri, json=data)

    @patch.object(
        pycpg.services.users.UserService,
        "_get_user_uid_by_id",
        return_value=TEST_USER_UID,
    )
    def test_reactivate_calls_post_with_expected_url_and_params(self, mock_connection):
        service = UserService(mock_connection)
        user_id = 12345
        service.reactivate(user_id, unblock_user=True)
        uri = f"{USER_URI_V3}/{TEST_USER_UID}/activate"
        data = {"unblock": True}
        mock_connection.post.assert_called_once_with(uri, json=data)

    @patch.object(
        pycpg.services.users.UserService,
        "_get_user_uid_by_id",
        return_value=TEST_USER_UID,
    )
    def test_change_org_assignment_calls_post_with_url_and_params(
        self, mock_connection
    ):
        service = UserService(mock_connection)
        user_id = 12345
        org_id = 67890
        service.change_org_assignment(user_id, org_id)
        uri = f"{USER_URI_V3}/{TEST_USER_UID}/move"
        data = {"orgId": org_id}
        mock_connection.post.assert_called_once_with(uri, json=data)

    def test_get_user_uid_by_id_calls_get_with_expected_uri_and_returns_uid(
        self, mock_connection, mock_get_user_by_id_response
    ):
        user_id = 12345
        service = UserService(mock_connection)
        mock_connection.get.return_value = mock_get_user_by_id_response
        uid = service._get_user_uid_by_id(user_id)
        uri = f"/api/v1/User/{user_id}"
        mock_connection.get.assert_called_once_with(uri, params={})
        assert uid == TEST_USER_UID

    def test_get_current_calls_get_with_expected_uri(self, mock_connection):
        service = UserService(mock_connection)
        service.get_current()
        uri = "/api/v1/User/my"
        mock_connection.get.assert_called_once_with(uri, params={})

    def test_get_current_raises_error_about_api_clients_if_user_not_found(
        self, mock_connection, mocker
    ):
        service = UserService(mock_connection)
        mock_connection.get.side_effect = create_mock_error(
            PycpgNotFoundError,
            mocker,
            """[{"name":"SYSTEM","description":"User not found"}]""",
        )
        with pytest.raises(PycpgNotFoundError) as err:
            service.get_current()
        assert (
            "User not found.  Please be aware that this method is incompatible with api client authentication."
        ) in str(err.value)
