import pytest
import requests

from py42.services.storage.exfiltrateddata import ExfiltratedDataService


class TestExfiltratedDataService:
    @pytest.fixture
    def mock_request(self, mocker):
        request = mocker.patch.object(requests, "get")
        request.return_value = b"stream"
        return request

    def test_get_download_token_calls_get_with_valid_params(
        self, mock_successful_connection
    ):
        service = ExfiltratedDataService(
            mock_successful_connection, mock_successful_connection
        )
        service.get_download_token(
            "testeventid", "testdeviceid", "testfilepath", "testSHA256", 1223
        )
        qry = "deviceUid=testdeviceid&eventId=testeventid&filePath=testfilepath&fileSHA256=testSHA256&versionTimestamp=1223"
        expected = f"api/v1/file-download-token?{qry}"
        mock_successful_connection.get.assert_called_once_with(
            expected, headers={"Accept": "*/*"}
        )

    def test_get_file_calls_get_with_valid_params(
        self, mock_successful_connection, mock_request
    ):
        mock_successful_connection.host_address = "https://example.com"
        service = ExfiltratedDataService(
            mock_successful_connection, mock_successful_connection
        )
        service.get_file("testtoken")
        mock_successful_connection.get.assert_called_once_with(
            "https://example.com/api/v1/get-file",
            headers={"Accept": "*/*"},
            params={"token": "testtoken"},
            stream=True,
        )
