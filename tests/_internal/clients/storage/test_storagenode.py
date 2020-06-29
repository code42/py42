import pytest
import requests
from py42._internal.clients.storage.storagenode import StoragePreservationDataClient


class TestStoragePreservationDataClient(object):
    @pytest.fixture
    def mock_session(self, mock_session, successful_response):
        mock_session.get.return_value = successful_response
        return mock_session

    @pytest.fixture
    def mock_request(self, mocker):
        request = mocker.patch.object(requests, "get")
        request.return_value = b"stream"
        return request

    def test_get_download_token_calls_get_with_valid_params(self, mock_session):
        client = StoragePreservationDataClient(mock_session)
        client.get_download_token("abc", "fabc", 1223)

        mock_session.get.assert_called_once_with(
            u"c42api/v3/FileDownloadToken",
            params={u"archiveGuid": "abc", u"fileId": "fabc", u"versionTimestamp": 1223,},
        )

    def test_get_file_calls_get_with_valid_params_with_substitution(
        self, mock_session, mock_request
    ):
        mock_session.host_address = "https://host.com"

        client = StoragePreservationDataClient(mock_session)
        client.get_file("token")
        mock_request.assert_called_once_with(
            "https://host.com/c42api/v3/GetFile", params={"PDSDownloadToken": "token"}, stream=True
        )

    def test_get_file_calls_get_with_valid_params(self, mock_session, mock_request):
        mock_session.host_address = "https://host.com"
        client = StoragePreservationDataClient(mock_session)
        client.get_file("PDSDownloadToken=token")
        mock_request.assert_called_once_with(
            "https://host.com/c42api/v3/GetFile", params={"PDSDownloadToken": "token"}, stream=True
        )
