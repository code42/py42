import pytest

from py42.services.preservationdata import PreservationDataService


class TestPreservationDataService(object):
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
            posted_data[u"fileSHA256"] == "adfadf"
            and posted_data[u"fileMD5"] == "abc"
            and posted_data[u"devicePaths"][0] == "/path/path"
            and posted_data[u"devicePaths"][1] == "/path/path2"
        )

    def test_get_file_version_list_uses_expected_url(self, mock_connection):
        pds = PreservationDataService(mock_connection)
        pds.get_file_version_list("testguid", "testmd5", "testsha256", "/t/1 X")
        qry = "fileSHA256=testsha256&fileMD5=testmd5&deviceUid=testguid&filePath=/t/1%20X"
        expected = "/api/v2/file-version-listing?{}".format(qry)
        mock_connection.get.assert_called_once_with(expected)
