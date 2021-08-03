import pytest
import requests

from py42.services.storage.exfiltrateddata import ExfiltratedDataService


class TestExfiltratedDataService(object):
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
        service.get_download_token("testeventid", "testdeviceid", "testfilepath", 1223)

        mock_successful_connection.get.assert_called_once_with(
            u"api/v1/file-download-token",
            params={
                u"eventId": "testeventid",
                u"deviceUid": "testdeviceid",
                u"filePath": "testfilepath",
                u"versionTimestamp": 1223
            },
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
