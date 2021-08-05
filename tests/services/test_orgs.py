# -*- coding: utf-8 -*-
import pytest
from tests.conftest import create_mock_response

import py42.settings
from py42.services.orgs import OrgService

COMPUTER_URI = "/api/Org"

MOCK_GET_ORG_RESPONSE = (
    """{"totalCount": 3000, "orgs": [{"orgName": "foo", "orgUid": "123"}]}"""
)

MOCK_EMPTY_GET_ORGS_RESPONSE = """{"totalCount": 3000, "orgs": []}"""


class TestOrgService(object):
    @pytest.fixture
    def mock_get_all_response(self, mocker):
        yield create_mock_response(mocker, MOCK_GET_ORG_RESPONSE)

    @pytest.fixture
    def mock_get_all_empty_response(self, mocker):
        yield create_mock_response(mocker, MOCK_EMPTY_GET_ORGS_RESPONSE)

    def test_get_org_by_id_calls_get_with_uri_and_params(
        self, mock_connection, successful_response
    ):
        mock_connection.get.return_value = successful_response
        service = OrgService(mock_connection)
        service.get_by_id(12345)
        uri = "{}/{}".format(COMPUTER_URI, 12345)
        mock_connection.get.assert_called_once_with(uri, params={})

    def test_get_all_calls_get_expected_number_of_times(
        self, mock_connection, mock_get_all_response, mock_get_all_empty_response
    ):
        py42.settings.items_per_page = 1
        service = OrgService(mock_connection)
        mock_connection.get.side_effect = [
            mock_get_all_response,
            mock_get_all_response,
            mock_get_all_empty_response,
        ]
        for _ in service.get_all():
            pass
        py42.settings.items_per_page = 500
        assert mock_connection.get.call_count == 3

    def test_get_page_calls_get_with_expected_url_and_params(self, mock_connection):
        service = OrgService(mock_connection)
        service.get_page(3, 25)
        mock_connection.get.assert_called_once_with(
            "/api/Org", params={"pgNum": 3, "pgSize": 25}
        )

    def test_get_agent_state_calls_get_with_uri_and_params(
        self, mock_connection, successful_response
    ):
        mock_connection.get.return_value = successful_response
        service = OrgService(mock_connection)
        service.get_agent_state("ORG_ID", property_name="KEY")
        expected_params = {"orgId": "ORG_ID", "propertyName": "KEY"}
        uri = u"/api/v14/agent-state/view-by-organization-id"
        mock_connection.get.assert_called_once_with(uri, params=expected_params)

    def test_get_agent_full_disk_access_states_calls_get_agent_state_with_arguments(
        self, mock_connection, successful_response, mocker
    ):
        mock_connection.get.return_value = successful_response
        service = OrgService(mock_connection)
        service.get_agent_state = mocker.Mock()
        service.get_agent_full_disk_access_states("ORG_ID")
        service.get_agent_state.assert_called_once_with("ORG_ID", "fullDiskAccess")
