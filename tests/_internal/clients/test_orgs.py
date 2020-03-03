# -*- coding: utf-8 -*-

import pytest
from requests import Response

import py42
from py42._internal.clients.orgs import OrgClient

COMPUTER_URI = "/api/Org"

MOCK_GET_ORG_RESPONSE = """{
  "data": {"totalCount": 3000, "orgs":["foo"]} 
}"""

MOCK_EMPTY_GET_ORGS_RESPONSE = """{
  "data": {"totalCount": 3000, "orgs":[]} 
}"""


class TestOrgClient(object):
    @pytest.fixture
    def mock_get_orgs_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = MOCK_GET_ORG_RESPONSE
        return response

    @pytest.fixture
    def mock_get_orgs_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = MOCK_EMPTY_GET_ORGS_RESPONSE
        return response

    def test_get_org_by_id_calls_get_with_uri_and_params(self, session):
        client = OrgClient(session)
        client.get_org_by_id("ORG_ID")
        uri = "{0}/{1}".format(COMPUTER_URI, "ORG_ID")
        session.get.assert_called_once_with(uri)

    def test_get_orgs_calls_get_expected_number_of_times(
        self, session, mock_get_orgs_response, mock_get_orgs_empty_response
    ):
        py42.settings.items_per_page = 1
        client = OrgClient(session)
        session.get.side_effect = [
            mock_get_orgs_response,
            mock_get_orgs_response,
            mock_get_orgs_empty_response,
        ]
        for page in client.get_orgs():
            pass
        py42.settings.items_per_page = 1000
        assert session.get.call_count == 3
