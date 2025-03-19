from unittest.mock import patch

import pytest
from tests.conftest import create_mock_error
from tests.conftest import create_mock_response

import pycpg.settings
from pycpg.exceptions import PycpgInternalServerError
from pycpg.services.orgs import OrgService

COMPUTER_URI = "/api/v1/Org"
ORGS_V3_URI = "/api/v3/orgs"
TEST_ORG_GUID = "12345-org-guid"

MOCK_GET_ORG_RESPONSE = """{"totalCount": 3000, "orgs": [{"orgName": "foo", "orgId": "12345", "orgUid": "123", "orgGuid":"12345-org-guid"}]}"""

MOCK_EMPTY_GET_ORGS_RESPONSE = """{"totalCount": 3000, "orgs": []}"""


class TestOrgService:
    @pytest.fixture
    def mock_get_page_response(self, mocker):
        return create_mock_response(mocker, MOCK_GET_ORG_RESPONSE)

    @pytest.fixture
    def mock_get_all_response(self, mocker):
        yield create_mock_response(mocker, MOCK_GET_ORG_RESPONSE)

    @pytest.fixture
    def mock_get_all_empty_response(self, mocker):
        yield create_mock_response(mocker, MOCK_EMPTY_GET_ORGS_RESPONSE)

    @patch.object(
        pycpg.services.orgs.OrgService,
        "_get_guid_by_id",
        return_value="org-guid-123",
    )
    def test_get_org_by_id_calls_get_with_uri_and_params(
        self, mock_connection, successful_response
    ):
        mock_connection.get.return_value = successful_response
        service = OrgService(mock_connection)
        service.get_by_id(12345)
        uri = f"{ORGS_V3_URI}/org-guid-123"
        mock_connection.get.assert_called_once_with(uri, params={})

    def test_get_all_calls_get_expected_number_of_times(
        self, mock_connection, mock_get_all_response, mock_get_all_empty_response
    ):
        pycpg.settings.items_per_page = 1
        service = OrgService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_response,
            mock_get_all_response,
            mock_get_all_empty_response,
        ]
        for _ in service.get_all():
            pass
        pycpg.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_page_calls_get_with_expected_url_and_params(self, mock_connection):
        service = OrgService(mock_connection)
        service.get_page(3, 25)
        mock_connection.get.assert_called_once_with(
            "/api/v1/Org", params={"pgNum": 3, "pgSize": 25}
        )

    def test_get_agent_state_calls_get_with_uri_and_params(
        self, mock_connection, successful_response
    ):
        mock_connection.get.return_value = successful_response
        service = OrgService(mock_connection)
        service.get_agent_state("ORG_ID", property_name="KEY")
        expected_params = {"orgId": "ORG_ID", "propertyName": "KEY"}
        uri = "/api/v14/agent-state/view-by-organization-id"
        mock_connection.get.assert_called_once_with(uri, params=expected_params)

    def test_get_agent_full_disk_access_states_calls_get_agent_state_with_arguments(
        self, mock_connection, successful_response, mocker
    ):
        mock_connection.get.return_value = successful_response
        service = OrgService(mock_connection)
        service.get_agent_state = mocker.Mock()
        service.get_agent_full_disk_access_states("ORG_ID")
        service.get_agent_state.assert_called_once_with("ORG_ID", "fullDiskAccess")

    @patch.object(
        pycpg.services.orgs.OrgService,
        "_get_guid_by_id",
        return_value="parent-guid-123",
    )
    def test_create_org_calls_post_with_expected_uri_and_params(self, mock_connection):
        service = OrgService(mock_connection)
        service.create_org(
            "My New Org",
            org_ext_ref="Org Ext Ref",
            notes="my org notes.",
            parent_org_uid="parent-123",
        )
        data = {
            "orgName": "My New Org",
            "orgExtRef": "Org Ext Ref",
            "notes": "my org notes.",
            "parentOrgGuid": "parent-guid-123",
        }
        mock_connection.post.assert_called_once_with(ORGS_V3_URI, json=data)

    @patch.object(
        pycpg.services.orgs.OrgService,
        "_get_guid_by_id",
        return_value="org-guid-123",
    )
    def test_get_by_uid_calls_get_with_expected_uri_and_params(self, mock_connection):
        service = OrgService(mock_connection)
        service.get_by_uid("UID-12345")
        uri = f"{ORGS_V3_URI}/org-guid-123"
        mock_connection.get.assert_called_once_with(uri, params={})

    @patch.object(
        pycpg.services.orgs.OrgService,
        "_get_guid_by_id",
        return_value=TEST_ORG_GUID,
    )
    def test_block_calls_post_with_expected_uri_and_params(self, mock_connection):
        service = OrgService(mock_connection)
        service.block(12345)
        uri = f"{ORGS_V3_URI}/{TEST_ORG_GUID}/block"
        mock_connection.post.assert_called_once_with(uri)

    @patch.object(
        pycpg.services.orgs.OrgService,
        "_get_guid_by_id",
        return_value=TEST_ORG_GUID,
    )
    def test_unblock_calls_post_with_expected_uri_and_params(self, mock_connection):
        service = OrgService(mock_connection)
        service.unblock(12345)
        uri = f"{ORGS_V3_URI}/{TEST_ORG_GUID}/unblock"
        mock_connection.post.assert_called_once_with(uri)

    @patch.object(
        pycpg.services.orgs.OrgService,
        "_get_guid_by_id",
        return_value=TEST_ORG_GUID,
    )
    def test_deactivate_calls_post_with_expected_uri_and_params(self, mock_connection):
        service = OrgService(mock_connection)
        service.deactivate(12345)
        uri = f"{ORGS_V3_URI}/{TEST_ORG_GUID}/deactivate"
        mock_connection.post.assert_called_once_with(uri)

    @patch.object(
        pycpg.services.orgs.OrgService,
        "_get_guid_by_id",
        return_value=TEST_ORG_GUID,
    )
    def test_reactivate_calls_post_with_expected_uri_and_params(self, mock_connection):
        service = OrgService(mock_connection)
        service.reactivate(12345)
        uri = f"{ORGS_V3_URI}/{TEST_ORG_GUID}/activate"
        mock_connection.post.assert_called_once_with(uri)

    def test_get_current_calls_get_with_expected_uri_and_params(self, mock_connection):
        service = OrgService(mock_connection)
        service.get_current()
        uri = f"{COMPUTER_URI}/my"
        mock_connection.get.assert_called_once_with(uri, params={})

    def test_get_current_returns_note_about_api_client_support_when_internal_server_error(
        self, mock_connection, mocker
    ):
        service = OrgService(mock_connection)
        mock_connection.get.side_effect = create_mock_error(
            PycpgInternalServerError, mocker, "Server Error"
        )
        with pytest.raises(PycpgInternalServerError) as err:
            service.get_current()

        expected = "Please be aware that this method is incompatible with api client authentication."
        assert expected in err.value.args[0]

    @patch.object(
        pycpg.services.orgs.OrgService,
        "_get_guid_by_id",
        return_value=TEST_ORG_GUID,
    )
    def test_update_org_calls_put_with_expected_uri_and_params(self, mock_connection):
        service = OrgService(mock_connection)
        service.update_org(
            12345, name="new org name", notes="new org notes", ext_ref="123"
        )
        uri = f"{ORGS_V3_URI}/{TEST_ORG_GUID}"
        data = {"orgName": "new org name", "orgExtRef": "123", "notes": "new org notes"}
        mock_connection.put.assert_called_once_with(uri, json=data)
