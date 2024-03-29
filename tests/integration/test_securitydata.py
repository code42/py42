from datetime import datetime
from datetime import timedelta

import pytest
from tests.integration.conftest import assert_successful_response

from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters import EventTimestamp
from py42.util import convert_datetime_to_epoch


@pytest.fixture(scope="module")
def md5_hash(request):
    return request.config.getini("md5_hash")


@pytest.fixture(scope="module")
def sha256_hash(request):
    return request.config.getini("sha256_hash")


@pytest.fixture(scope="module")
def user_uid(request):
    return request.config.getini("user_uid")


@pytest.fixture
def file_data(request):
    return request.config.getini("file_data")


@pytest.mark.integration
class TestSecurityData:
    def test_search_file_events(self, connection):
        start_date = datetime.utcnow() - timedelta(1)
        end_date = datetime.utcnow()
        start_timestamp = convert_datetime_to_epoch(start_date)
        end_timestamp = convert_datetime_to_epoch(end_date)
        date_query = EventTimestamp.in_range(start_timestamp, end_timestamp)
        query = FileEventQuery.all(date_query)
        response = connection.securitydata.search_file_events(query)
        assert_successful_response(response)

    def test_stream_file_by_md5(self, connection, md5_hash, file_data):
        response = connection.securitydata.stream_file_by_md5(md5_hash)
        assert str(response) == file_data

    def test_stream_file_by_sha256(self, connection, sha256_hash, file_data):
        response = connection.securitydata.stream_file_by_sha256(sha256_hash)
        assert str(response) == file_data
