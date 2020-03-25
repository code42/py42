# -*- coding: utf-8 -*-
import json

import pytest
from requests import Response

import py42
import py42.sdk.settings
from py42.clients.orgs import OrgClient
from py42.sdk.response import Py42Response

COMPUTER_URI = "/api/Org"

MOCK_GET_ORG_RESPONSE = """{"totalCount": 3000, "orgs": [{"orgName": "foo", "orgUid": "123"}]}"""

MOCK_EMPTY_GET_ORGS_RESPONSE = """{"totalCount": 3000, "orgs": []}"""


class TestOrgClient(object):
    @pytest.fixture
    def mock_get_orgs_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_GET_ORG_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_orgs_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_EMPTY_GET_ORGS_RESPONSE
        return Py42Response(response)

    def test_get_org_by_id_calls_get_with_uri_and_params(self, mock_session, successful_response):
        mock_session.get.return_value = successful_response
        client = OrgClient(mock_session)
        client.get_by_id("ORG_ID")
        uri = "{0}/{1}".format(COMPUTER_URI, "ORG_ID")
        mock_session.get.assert_called_once_with(uri, params={})

    def test_get_orgs_calls_get_expected_number_of_times(
        self, mock_session, mock_get_orgs_response, mock_get_orgs_empty_response
    ):
        py42.sdk.settings.items_per_page = 1
        client = OrgClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_orgs_response,
            mock_get_orgs_response,
            mock_get_orgs_empty_response,
        ]
        for _ in client.get_all():
            pass
        py42.sdk.settings.items_per_page = 1000
        assert mock_session.get.call_count == 3

    def test_get_org_by_name_returns_expected_org(
        self, mock_session, mock_get_orgs_response, mock_get_orgs_empty_response
    ):
        py42.sdk.settings.items_per_page = 1
        client = OrgClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_orgs_response,
            mock_get_orgs_response,
            mock_get_orgs_empty_response,
        ]
        actual = client.get_by_name("foo")[0]
        py42.sdk.settings.items_per_page = 1000
        assert actual["orgUid"] == "123"

    def test_get_org_by_name_returns_expected_number_of_orgs(
        self, mock_session, mock_get_orgs_response, mock_get_orgs_empty_response
    ):
        py42.sdk.settings.items_per_page = 1
        client = OrgClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_orgs_response,
            mock_get_orgs_response,
            mock_get_orgs_empty_response,
        ]
        actual = len(client.get_by_name("foo"))
        py42.sdk.settings.items_per_page = 1000
        assert actual == 2

    def test_get_org_by_name_when_not_found_returns_empty_list(
        self, mock_session, mock_get_orgs_response, mock_get_orgs_empty_response
    ):
        client = OrgClient(mock_session)
        mock_session.get.return_value = mock_get_orgs_empty_response
        actual = client.get_by_name("foo")
        assert actual == []
