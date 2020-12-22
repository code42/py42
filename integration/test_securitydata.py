from datetime import datetime
from datetime import timedelta

import pytest

from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters import EventTimestamp

user_uid = 984118686188300065
md5_hash = "202cb962ac59075b964b07152d234b70"
sha256_hash = "a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3"


@pytest.fixture
def plan_info(connection):
    plans = connection.securitydata.get_security_plan_storage_info_list(user_uid)
    return plans[0]


def test_get_all_plan_security_events(connection, plan_info):
    response_gen = connection.securitydata.get_all_plan_security_events(plan_info)
    for response in response_gen:
        assert response[0].status_code == 200
        break


def test_get_all_user_security_events(connection):
    response_gen = connection.securitydata.get_all_user_security_events(user_uid)
    for response in response_gen:
        assert response[0].status_code == 200
        break


def test_search_file_events(connection):
    start_date = datetime.utcnow() - timedelta(1)
    end_date = datetime.utcnow()
    date_query = EventTimestamp.in_range(start_date.timestamp(), end_date.timestamp())
    query = FileEventQuery.all(date_query)
    response = connection.securitydata.search_file_events(query)
    assert response.status_code == 200


def test_stream_file_by_md5(connection):
    response = connection.securitydata.stream_file_by_md5(md5_hash)
    assert str(response) == "123"


def test_stream_file_by_sha256(connection):
    response = connection.securitydata.stream_file_by_sha256(sha256_hash)
    assert str(response) == "123"
