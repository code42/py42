from datetime import datetime
from datetime import timedelta

import pytest
from tests.integration.conftest import assert_successful_response

from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters import EventTimestamp


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


@pytest.fixture
def plan_info(connection, user_uid):
    plans = connection.securitydata.get_security_plan_storage_info_list(user_uid)
    return plans[0]


@pytest.mark.integration
class TestSecurityData:
    def test_get_all_plan_security_events(self, connection, plan_info):
        response_gen = connection.securitydata.get_all_plan_security_events(plan_info)
        for response in response_gen:
            assert_successful_response(response[0])
            break

    def test_get_all_user_security_events(self, connection, user_uid):
        response_gen = connection.securitydata.get_all_user_security_events(user_uid)
        for response in response_gen:
            assert_successful_response(response[0])
            break

    def test_search_file_events(self, connection):
        start_date = datetime.utcnow() - timedelta(1)
        end_date = datetime.utcnow()
        date_query = EventTimestamp.in_range(
            start_date.timestamp(), end_date.timestamp()
        )
        query = FileEventQuery.all(date_query)
        response = connection.securitydata.search_file_events(query)
        assert_successful_response(response)

    def test_stream_file_by_md5(self, connection, md5_hash, file_data):
        response = connection.securitydata.stream_file_by_md5(md5_hash)
        assert str(response) == file_data

    def test_stream_file_by_sha256(self, connection, sha256_hash, file_data):
        response = connection.securitydata.stream_file_by_sha256(sha256_hash)
        assert str(response) == file_data
