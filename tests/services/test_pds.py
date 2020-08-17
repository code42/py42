import pytest

from py42.services.preservationdata import PreservationDataService


class TestPreservationDataServiceClient(object):
    @pytest.fixture
    def mock_connection(self, mock_connection, successful_response):
        mock_connection.post.return_value = successful_response
        return mock_connection

    def test_find_file_versions_posts_expected_data(self, mock_connection):
        pds = PreservationDataService(mock_connection)
        pds.find_file_versions("abc", "adfadf", "test", "path/path")

        assert mock_connection.post.call_count == 1
        posted_data = mock_connection.post.call_args[1]["json"]
        assert mock_connection.post.call_args[0][0] == "/api/v1/FindAvailableVersion"
        assert (
            posted_data[u"fileSHA256"] == "adfadf"
            and posted_data[u"fileMD5"] == "abc"
            and posted_data[u"devicePaths"][0][u"deviceGuid"] == "test"
            and posted_data[u"devicePaths"][0][u"paths"] == "path/path"
        )
