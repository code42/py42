import pytest

from py42.services.preservationdata import PreservationDataService


class TestPreservationDataService:
    @pytest.fixture
    def mock_connection(self, mock_connection, successful_response):
        mock_connection.post.return_value = successful_response
        return mock_connection

    def test_find_file_version_posts_expected_data(self, mock_connection):
        pds = PreservationDataService(mock_connection)
        pds.find_file_version("abc", "adfadf", ["/path/path", "/path/path2"])

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_args[0][0] == "/api/v1/FindAvailableVersion"
        assert (
            posted_data["fileSHA256"] == "adfadf"
            and posted_data["fileMD5"] == "abc"
            and posted_data["devicePaths"][0] == "/path/path"
            and posted_data["devicePaths"][1] == "/path/path2"
        )

    def test_get_file_version_list_uses_expected_ur(self, mock_connection):
        pds = PreservationDataService(mock_connection)
        pds.get_file_version_list("testguid", "testmd5", "testsha256", "/t/1 X")
        qry = "fileSHA256=testsha256&fileMD5=testmd5&deviceGuid=testguid&path=/t/1%20X"
        expected = f"/api/v1/FileVersionListing?{qry}"
        mock_connection.get.assert_called_once_with(expected)
