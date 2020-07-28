import pytest

from py42._internal.clients.pds import PreservationDataServiceClient


class TestPreservationDataServiceClient(object):
    @pytest.fixture
    def mock_session(self, mock_session, successful_response):
        mock_session.post.return_value = successful_response
        return mock_session

    def test_find_file_versions_posts_expected_data(self, mock_session):
        pds = PreservationDataServiceClient(mock_session)
        pds.find_file_versions("abc", "adfadf", "test", "path/path")

        assert mock_session.post.call_count == 1
        posted_data = mock_session.post.call_args[1]["json"]
        assert mock_session.post.call_args[0][0] == "/api/v1/FindAvailableVersion"
        assert (
            posted_data[u"fileSHA256"] == "adfadf"
            and posted_data[u"fileMD5"] == "abc"
            and posted_data[u"devicePaths"][0][u"deviceGuid"] == "test"
            and posted_data[u"devicePaths"][0][u"paths"] == "path/path"
        )
