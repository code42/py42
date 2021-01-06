import pytest
from requests import Response

import py42.settings
from py42.response import Py42Response
from py42.services.cases import CasesService


GET_ALL_TEST_RESPONSE = """{"cases":["test"], "totalCount":1}"""
EMPTY_GET_ALL_TEST_RESPONSE = """{"cases": [], "totalCount":0}"""

_TEST_CASE_NUMBER = 123456
_BASE_URI = u"/api/v1/case"


class TestCasesService:
    @pytest.fixture
    def mock_case_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = GET_ALL_TEST_RESPONSE
        return Py42Response(response)

    @pytest.fixture
    def mock_case_empty_response(self, mocker):
        response = mocker.MagicMock(spec=Response)
        response.status_code = 200
        response.text = EMPTY_GET_ALL_TEST_RESPONSE
        return Py42Response(response)

    def test_create_called_with_expected_url_and_params(self, mock_connection):
        cases_service = CasesService(mock_connection)
        cases_service.create(
            u"name", u"subject", u"user uid", u"description", u"findings"
        )
        assert mock_connection.post.call_args[0][0] == u"/api/v1/case"
        data = {
            "name": u"name",
            "subject": u"subject",
            "assignee": u"user uid",
            "description": u"description",
            "findings": u"findings",
        }
        mock_connection.post.assert_called_once_with(_BASE_URI, json=data)

    def test_get_all_called_expected_number_of_times(
        self, mock_connection, mock_case_response, mock_case_empty_response
    ):
        cases_service = CasesService(mock_connection)
        py42.settings.items_per_page = 1
        items = [mock_case_response, mock_case_empty_response]

        mock_connection.get.side_effect = items
        for _ in cases_service.get_all():
            pass

        assert mock_connection.get.call_count == 2
        py42.settings.items_per_page = 500

    def test_get_all_called_with_expected_url_and_default_params(
        self, mock_connection, mock_case_response, mock_case_empty_response
    ):
        cases_service = CasesService(mock_connection)
        items = [
            mock_case_response,
        ]

        mock_connection.get.side_effect = items
        for _ in cases_service.get_all():
            pass

        expected_params = {
            "name": None,
            "subject": None,
            "assignee": None,
            "createdAt": None,
            "updatedAt": None,
            "status": None,
            "pgNum": 1,
            "pgSize": 500,
            "srtDir": "asc",
            "srtKey": "number",
        }
        mock_connection.get.assert_called_once_with(_BASE_URI, params=expected_params)

    def test_get_all_called_with_expected_url_and_params(
        self, mock_connection, mock_case_response
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.get.side_effect = [
            mock_case_response,
            mock_case_response,
        ]
        for _ in cases_service.get_all(name="test-case"):
            continue

        expected_params = {
            "name": "test-case",
            "subject": None,
            "assignee": None,
            "createdAt": None,
            "updatedAt": None,
            "status": None,
            "pgNum": 1,
            "pgSize": 500,
            "srtDir": "asc",
            "srtKey": "number",
        }
        mock_connection.get.assert_called_once_with(_BASE_URI, params=expected_params)

    def test_get_all_called_with_expected_url_and_all_optional_params(
        self, mock_connection, mock_case_response
    ):
        cases_service = CasesService(mock_connection)
        mock_connection.get.side_effect = [
            mock_case_response,
            mock_case_response,
        ]
        for _ in cases_service.get_all(
            name="test-case",
            subject="test",
            assignee="user-uid",
            updated_at="2010-04-30T001",
            created_at="2010-01-03T002",
            status="open",
        ):
            continue

        expected_params = {
            "name": "test-case",
            "subject": "test",
            "assignee": "user-uid",
            "createdAt": "2010-01-03T002",
            "updatedAt": "2010-04-30T001",
            "status": "open",
            "pgNum": 1,
            "pgSize": 500,
            "srtDir": "asc",
            "srtKey": "number",
        }
        mock_connection.get.assert_called_once_with(_BASE_URI, params=expected_params)

    def test_export_called_with_expected_url_and_params(self, mock_connection):
        cases_service = CasesService(mock_connection)
        cases_service.export_summary(_TEST_CASE_NUMBER)
        assert mock_connection.get.call_args[0][0] == u"/api/v1/case/{}/export".format(
            _TEST_CASE_NUMBER
        )

    def test_get_case_called_with_expected_url_and_params(self, mock_connection):
        cases_service = CasesService(mock_connection)
        cases_service.get_case(_TEST_CASE_NUMBER)
        assert mock_connection.get.call_args[0][0] == u"/api/v1/case/{}".format(
            _TEST_CASE_NUMBER
        )

    def test_update_called_with_expected_url_and_params(self, mock_connection):
        cases_service = CasesService(mock_connection)
        cases_service.update(_TEST_CASE_NUMBER, findings=u"x")
        data = {
            "name": None,
            "subject": None,
            "assignee": None,
            "description": None,
            "findings": u"x",
        }
        mock_connection.put.assert_called_once_with(
            u"/api/v1/case/{}".format(_TEST_CASE_NUMBER), json=data
        )
