import pytest
import requests

from py42.services.storage.preservationdata import StoragePreservationDataService


class TestStoragePreservationDataService(object):
    @pytest.fixture
    def mock_request(self, mocker):
        request = mocker.patch.object(requests, "get")
        request.return_value = b"stream"
        return request

    def test_get_download_token_calls_get_with_valid_params(
        self, mock_successful_connection
    ):
        service = StoragePreservationDataService(
            mock_successful_connection, mock_successful_connection
        )
        service.get_download_token("abc", "fabc", 1223)

        mock_successful_connection.get.assert_called_once_with(
            u"c42api/v3/FileDownloadToken",
            params={
                u"archiveGuid": "abc",
                u"fileId": "fabc",
                u"versionTimestamp": 1223,
            },
        )

    def test_get_file_calls_get_with_valid_params_with_substitution(
        self, mock_successful_connection, mock_request
    ):
        mock_successful_connection.host_address = "https://host.com"

        service = StoragePreservationDataService(
            mock_successful_connection, mock_successful_connection
        )
        service.get_file("token")
        mock_successful_connection.get.assert_called_once_with(
            "https://host.com/c42api/v3/GetFile",
            headers={"Accept": "*/*"},
            params={"PDSDownloadToken": "token"},
            stream=True,
        )

    def test_get_file_calls_get_with_valid_params(
        self, mock_successful_connection, mock_request
    ):
        mock_successful_connection.host_address = "https://host.com"
        service = StoragePreservationDataService(
            mock_successful_connection, mock_successful_connection
        )
        service.get_file("PDSDownloadToken=token")
        mock_successful_connection.get.assert_called_once_with(
            "https://host.com/c42api/v3/GetFile",
            headers={"Accept": "*/*"},
            params={"PDSDownloadToken": "token"},
            stream=True,
        )
