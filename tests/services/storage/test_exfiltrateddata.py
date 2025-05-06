import pytest
import requests

from py42.services.storage.exfiltrateddata import ExfiltratedDataService


class TestExfiltratedDataService:
    @pytest.fixture
    def mock_request(self, mocker):
        request = mocker.patch.object(requests, "get")
        request.return_value = b"stream"
        return request

    def test_get_file_calls_get_with_valid_params(
        self, mock_successful_connection, mock_request
    ):
        mock_successful_connection.host_address = "https://example.com"
        service = ExfiltratedDataService(
            mock_successful_connection, mock_successful_connection
        )
        service.get_file("https://example.com/testpath?token=testtoken")
        mock_successful_connection.get.assert_called_once_with(
            "https://example.com/testpath?token=testtoken",
            headers={"Accept": "*/*"},
            stream=True,
        )
