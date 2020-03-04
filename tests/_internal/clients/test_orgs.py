# -*- coding: utf-8 -*-

import pytest
from requests import Response

from py42._internal.clients.orgs import OrgClient
import py42

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

    def test_get_by_id_calls_get_with_uri_and_params(
        self, session, v3_required_session, mock_get_orgs_empty_response
    ):
        client = OrgClient(session, v3_required_session)
        session.get.return_value = mock_get_orgs_empty_response
        client.get_by_id("ORG_ID")
        uri = "{0}/{1}".format(COMPUTER_URI, "ORG_ID")
        session.get.assert_called_once_with(uri)

    def test_get_all_calls_get_expected_number_of_times(
        self, session, v3_required_session, mock_get_orgs_response, mock_get_orgs_empty_response
    ):
        py42.settings.items_per_page = 1
        client = OrgClient(session, v3_required_session)
        session.get.side_effect = [
            mock_get_orgs_response,
            mock_get_orgs_response,
            mock_get_orgs_empty_response,
        ]
        for _ in client.get_all():
            pass
        py42.settings.items_per_page = 1000
        assert session.get.call_count == 3
