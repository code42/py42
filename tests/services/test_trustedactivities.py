import json

import pytest
from tests.conftest import create_mock_error
from tests.conftest import create_mock_response

import py42.settings
from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42ConflictError
from py42.exceptions import Py42DescriptionLimitExceededError
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42TrustedActivityConflictError
from py42.exceptions import Py42TrustedActivityIdNotFound
from py42.exceptions import Py42TrustedActivityInvalidCharacterError
from py42.services.trustedactivities import TrustedActivitiesService

GET_ALL_TEST_RESPONSE = '{"trustResources":["test"], "totalCount":1}'
EMPTY_GET_ALL_TEST_RESPONSE = '{"trustResources": [], "totalCount":0}'
GET_TRUSTED_ACTIVITY_RESPONSE = {
    "description": "test description",
    "resourceId": "456",
    "type": "DOMAIN",
    "updatedAt": "2021-09-13T15:36:59.743Z",
    "updatedByUserUid": "user uid",
    "updatedByUsername": "username",
    "value": "domain.com",
}

_INVALID_RESOURCE_ID = 0
_TEST_TRUSTED_ACTIVITY_RESOURCE_ID = 123
_BASE_URI = "/api/v1/trusted-activities"
_DESCRIPTION_TOO_LONG_ERROR_MSG = (
    '{"problem":"DESCRIPTION_TOO_LONG","description":null}'
)
_CONFLICT_ERROR_MSG = '{"problem":"CONFLICT","description":null}'
_INVALID_CHANGE_ERROR_MSG = '{"problem":"INVALID_CHANGE","description":null}'
_INVALID_CHARACTER_ERROR_MSG = (
    '{"problem":"INVALID_CHARACTERS_IN_VALUE","description":null}'
)
_RESOURCE_ID_NOT_FOUND_ERROR_MSG = ""


@pytest.fixture
def mock_get_all_response(mocker):
    return create_mock_response(mocker, GET_ALL_TEST_RESPONSE)


@pytest.fixture
def mock_get_all_empty_response(mocker):
    return create_mock_response(mocker, EMPTY_GET_ALL_TEST_RESPONSE)


@pytest.fixture
def mock_get_response(mocker):
    data = json.dumps(GET_TRUSTED_ACTIVITY_RESPONSE)
    response = create_mock_response(mocker, data)
    return response


@pytest.fixture
def mock_long_description_error(mocker):
    return create_mock_error(
        Py42BadRequestError, mocker, _DESCRIPTION_TOO_LONG_ERROR_MSG
    )


@pytest.fixture
def mock_conflict_error(mocker):
    return create_mock_error(Py42ConflictError, mocker, _CONFLICT_ERROR_MSG)


@pytest.fixture
def mock_invalid_change_error(mocker):
    return create_mock_error(Py42BadRequestError, mocker, _INVALID_CHANGE_ERROR_MSG)


@pytest.fixture
def mock_invalid_character_error(mocker):
    return create_mock_error(Py42BadRequestError, mocker, _INVALID_CHARACTER_ERROR_MSG)


@pytest.fixture
def mock_resource_id_not_found_error(mocker):
    return create_mock_error(
        Py42NotFoundError, mocker, _RESOURCE_ID_NOT_FOUND_ERROR_MSG
    )


class TestTrustedActivitiesService:
    def test_create_called_with_expected_url_and_params(self, mock_connection):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        trusted_activities_service.create(
            "DOMAIN",
            "test.com",
        )
        assert mock_connection.post.call_args[0][0] == _BASE_URI
        data = {
            "type": "DOMAIN",
            "value": "test.com",
            "description": None,
        }
        mock_connection.post.assert_called_once_with(_BASE_URI, json=data)

    def test_create_called_with_expected_url_and_optional_params(self, mock_connection):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        trusted_activities_service.create("DOMAIN", "test.com", "description")
        assert mock_connection.post.call_args[0][0] == _BASE_URI
        data = {
            "type": "DOMAIN",
            "value": "test.com",
            "description": "description",
        }
        mock_connection.post.assert_called_once_with(_BASE_URI, json=data)

    def test_create_when_fails_with_name_conflict_error_raises_custom_exception(
        self, mock_connection, mock_conflict_error
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.post.side_effect = mock_conflict_error
        with pytest.raises(Py42TrustedActivityConflictError) as err:
            trusted_activities_service.create("DOMAIN", "duplicate-name")

        assert err.value.args[0] == (
            "Duplicate URL or workspace name, 'duplicate-name' already exists on your trusted list.  "
            "Please provide a unique value"
        )

    def test_create_when_fails_with_description_too_long_error_raises_custom_exception(
        self, mock_connection, mock_long_description_error
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.post.side_effect = mock_long_description_error
        with pytest.raises(Py42DescriptionLimitExceededError) as err:
            trusted_activities_service.create(
                "DOMAIN", "name", description="supposedly too long"
            )

        assert (
            err.value.args[0]
            == "Description limit exceeded, max 250 characters allowed."
        )

    def test_create_when_fails_with_invalid_character_error_raises_custom_exception(
        self, mock_connection, mock_invalid_character_error
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.post.side_effect = mock_invalid_character_error
        with pytest.raises(Py42TrustedActivityInvalidCharacterError) as err:
            trusted_activities_service.create("DOMAIN", "bad@name")

        assert (
            err.value.args[0] == "Invalid character in domain or Slack workspace name"
        )

    def test_get_all_called_expected_number_of_times(
        self, mock_connection, mock_get_all_response, mock_get_all_empty_response
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        py42.settings.items_per_page = 1
        items = [mock_get_all_response, mock_get_all_empty_response]

        mock_connection.get.side_effect = items
        for _ in trusted_activities_service.get_all():
            pass

        assert mock_connection.get.call_count == 2
        py42.settings.items_per_page = 500

    def test_get_all_called_with_expected_url_and_params(
        self, mock_connection, mock_get_all_response
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.get.side_effect = [mock_get_all_response]

        for _ in trusted_activities_service.get_all():
            pass

        assert mock_connection.get.call_args[0][0] == _BASE_URI
        data = {
            "type": None,
            "pgNum": 1,
            "pgSize": 500,
        }
        mock_connection.get.assert_called_once_with(_BASE_URI, params=data)

    def test_get_all_called_with_expected_url_and_all_optional_params(
        self, mock_connection, mock_get_all_response
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_response,
        ]

        for _ in trusted_activities_service.get_all("DOMAIN"):
            pass

        assert mock_connection.get.call_args[0][0] == _BASE_URI
        data = {
            "type": "DOMAIN",
            "pgNum": 1,
            "pgSize": 500,
        }
        mock_connection.get.assert_called_once_with(_BASE_URI, params=data)

    def test_get_called_with_expected_url_and_params(self, mock_connection):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        trusted_activities_service.get(_TEST_TRUSTED_ACTIVITY_RESOURCE_ID)
        expected_url = f"{_BASE_URI}/{_TEST_TRUSTED_ACTIVITY_RESOURCE_ID}"
        assert mock_connection.get.call_args[0][0] == expected_url
        mock_connection.get.assert_called_once_with(expected_url)

    def test_get_when_fails_with_resource_id_not_found_error_raises_custom_exception(
        self, mock_connection, mock_resource_id_not_found_error
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.get.side_effect = mock_resource_id_not_found_error
        with pytest.raises(Py42TrustedActivityIdNotFound) as err:
            trusted_activities_service.get(_INVALID_RESOURCE_ID)

        assert err.value.args[0] == f"Resource ID '{_INVALID_RESOURCE_ID}' not found."

    def test_update_called_with_expected_url_and_params(
        self, mock_connection, mock_get_response
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.get.return_value = mock_get_response
        trusted_activities_service.update(_TEST_TRUSTED_ACTIVITY_RESOURCE_ID)
        expected_url = f"{_BASE_URI}/{_TEST_TRUSTED_ACTIVITY_RESOURCE_ID}"
        assert mock_connection.put.call_args[0][0] == expected_url
        data = {
            "type": "DOMAIN",
            "value": "domain.com",
            "description": "test description",
        }
        mock_connection.put.assert_called_once_with(expected_url, json=data)

    def test_update_called_with_expected_url_and_optional_params(
        self, mock_connection, mock_get_response
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.get.return_value = mock_get_response
        trusted_activities_service.update(
            _TEST_TRUSTED_ACTIVITY_RESOURCE_ID, "test.com", "description"
        )
        expected_url = f"{_BASE_URI}/{_TEST_TRUSTED_ACTIVITY_RESOURCE_ID}"
        assert mock_connection.put.call_args[0][0] == expected_url
        data = {
            "type": "DOMAIN",
            "value": "test.com",
            "description": "description",
        }
        mock_connection.put.assert_called_once_with(expected_url, json=data)

    def test_update_when_fails_with_name_conflict_error_raises_custom_exception(
        self, mock_connection, mock_conflict_error, mock_get_response
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.get.return_value = mock_get_response
        mock_connection.put.side_effect = mock_conflict_error
        with pytest.raises(Py42TrustedActivityConflictError) as err:
            trusted_activities_service.update(
                _TEST_TRUSTED_ACTIVITY_RESOURCE_ID, value="duplicate-name"
            )

        assert err.value.args[0] == (
            "Duplicate URL or workspace name, 'duplicate-name' already exists on your trusted list.  "
            "Please provide a unique value"
        )

    def test_update_when_fails_with_description_too_long_error_raises_custom_exception(
        self, mock_connection, mock_get_response, mock_long_description_error
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.get.return_value = mock_get_response
        mock_connection.put.side_effect = mock_long_description_error
        with pytest.raises(Py42DescriptionLimitExceededError) as err:
            trusted_activities_service.update(
                _TEST_TRUSTED_ACTIVITY_RESOURCE_ID, description="supposedly too long"
            )

        assert (
            err.value.args[0]
            == "Description limit exceeded, max 250 characters allowed."
        )

    def test_update_when_fails_with_invalid_character_error_raises_custom_exception(
        self, mock_connection, mock_get_response, mock_invalid_character_error
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.get.return_value = mock_get_response
        mock_connection.put.side_effect = mock_invalid_character_error
        with pytest.raises(Py42TrustedActivityInvalidCharacterError) as err:
            trusted_activities_service.update(
                _TEST_TRUSTED_ACTIVITY_RESOURCE_ID, value="bad@name"
            )

        assert (
            err.value.args[0] == "Invalid character in domain or Slack workspace name"
        )

    def test_update_when_fails_with_resource_id_not_found_error_raises_custom_exception(
        self, mock_connection, mock_resource_id_not_found_error
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.put.side_effect = mock_resource_id_not_found_error
        with pytest.raises(Py42TrustedActivityIdNotFound) as err:
            trusted_activities_service.update(
                _INVALID_RESOURCE_ID, description="This id should not be found."
            )

        assert err.value.args[0] == f"Resource ID '{_INVALID_RESOURCE_ID}' not found."

    def test_delete_called_with_expected_url_and_params(self, mock_connection):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        trusted_activities_service.delete(_TEST_TRUSTED_ACTIVITY_RESOURCE_ID)
        expected_url = f"{_BASE_URI}/{_TEST_TRUSTED_ACTIVITY_RESOURCE_ID}"
        assert mock_connection.delete.call_args[0][0] == expected_url
        mock_connection.delete.assert_called_once_with(expected_url)

    def test_delete_when_fails_with_resource_id_not_found_error_raises_custom_exception(
        self, mock_connection, mock_resource_id_not_found_error
    ):
        trusted_activities_service = TrustedActivitiesService(mock_connection)
        mock_connection.delete.side_effect = mock_resource_id_not_found_error
        with pytest.raises(Py42TrustedActivityIdNotFound) as err:
            trusted_activities_service.delete(_INVALID_RESOURCE_ID)

        assert err.value.args[0] == f"Resource ID '{_INVALID_RESOURCE_ID}' not found."
