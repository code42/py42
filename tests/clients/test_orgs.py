# -*- coding: utf-8 -*-
import pytest
from requests import Response

import py42.settings
from py42.services.orgs import OrgClient
from py42.response import Py42Response

COMPUTER_URI = "/api/Org"

MOCK_GET_ORG_RESPONSE = (
    """{"totalCount": 3000, "orgs": [{"orgName": "foo", "orgUid": "123"}]}"""
)

MOCK_EMPTY_GET_ORGS_RESPONSE = """{"totalCount": 3000, "orgs": []}"""


class TestOrgClient(object):
    @pytest.fixture
    def mock_get_all_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_GET_ORG_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_get_all_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.encoding = "utf-8"
        response.text = MOCK_EMPTY_GET_ORGS_RESPONSE
        return Py42Response(response)

    def test_get_org_by_id_calls_get_with_uri_and_params(
        self, mock_session, successful_response
    ):
        mock_session.get.return_value = successful_response
        client = OrgClient(mock_session)
        client.get_by_id(12345)
        uri = "{}/{}".format(COMPUTER_URI, 12345)
        mock_session.get.assert_called_once_with(uri, params={})

    def test_get_all_calls_get_expected_number_of_times(
        self, mock_session, mock_get_all_response, mock_get_all_empty_response
    ):
        py42.settings.items_per_page = 1
        client = OrgClient(mock_session)
        mock_session.get.side_effect = [
            mock_get_all_response,
            mock_get_all_response,
            mock_get_all_empty_response,
        ]
        for _ in client.get_all():
            pass
        py42.settings.items_per_page = 500
        assert mock_session.get.call_count == 3

    def test_get_page_calls_get_with_expected_url_and_params(self, mock_session):
        client = OrgClient(mock_session)
        client.get_page(3, 25)
        mock_session.get.assert_called_once_with(
            "/api/Org", params={"pgNum": 3, "pgSize": 25}
        )
