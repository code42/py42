# -*- coding: utf-8 -*-

import pytest
from requests import Response

from py42._internal.clients.orgs import OrgClient
from py42._internal.session import Py42Session
import py42.settings as settings

COMPUTER_URI = "/api/Org"

MOCK_GET_ORG_RESPONSE = """{
  "data": {"totalCount": 3000, "orgs":["foo"]} 
}"""

MOCK_EMPTY_GET_ORGS_RESPONSE = """{
  "data": {"totalCount": 3000, "orgs":[]} 
}"""

settings.items_per_page = 1


class TestOrgClient(object):
    @pytest.fixture
    def session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def v3_required_session(self, mocker):
        return mocker.MagicMock(spec=Py42Session)

    @pytest.fixture
    def mock_get_orgs(self, mocker):
        def get_devices(*args, **kwargs):
            response = mocker.MagicMock(spec=Response)
            response.status_code = 200
            response.text = MOCK_GET_ORG_RESPONSE
            return response

        return get_devices

    @pytest.fixture
    def mock_get_orgs_empty(self, mocker):
        def get_devices(*args, **kwargs):
            response = mocker.MagicMock(spec=Response)
            response.status_code = 200
            response.text = MOCK_EMPTY_GET_ORGS_RESPONSE
            return response

        return get_devices

    def test_get_org_by_id_calls_get_with_uri_and_params(self, session, v3_required_session):
        client = OrgClient(session, v3_required_session)
        client.get_org_by_id("ORG_ID")
        uri = "{0}/{1}".format(COMPUTER_URI, "ORG_ID")
        session.get.assert_called_once_with(uri)

    def test_get_orgs_calls_get_expected_number_of_times(
        self, session, v3_required_session, mock_get_orgs, mock_get_orgs_empty
    ):
        client = OrgClient(session, v3_required_session)
        session.get.side_effect = [mock_get_orgs(), mock_get_orgs(), mock_get_orgs_empty()]
        for page in client.get_orgs():
            pass
        assert session.get.call_count == 3
