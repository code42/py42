import pytest

from py42.services.preservationdata import PreservationDataService


class TestPreservationDataService:
    @pytest.fixture
    def mock_connection(self, mock_connection, successful_response):
        mock_connection.post.return_value = successful_response
        return mock_connection

    def test_get_file_version_list_uses_expected_url(self, mock_connection):
        pds = PreservationDataService(mock_connection)
        pds.get_file_version_list("testguid", "testmd5", "testsha256", "/t/1 X")
        qry = (
            "fileSHA256=testsha256&fileMD5=testmd5&deviceUid=testguid&filePath=/t/1%20X"
        )
        expected = f"/api/v3/search-file?{qry}"
        mock_connection.get.assert_called_once_with(expected)
