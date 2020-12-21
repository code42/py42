from datetime import datetime
from datetime import timezone

import pytest

from py42.exceptions import Py42Error
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters import EventTimestamp

user_uid = 984118686188300065
md5_hash = "fe78649ad786c2fa1fd66b6a6db00030"
sha256_hash = "9d777e0031bfb10a15128ebcd01eeb062c373f69229058774ca2d596744475ac"


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
    start_date = datetime(2020, 9, 13, tzinfo=timezone.utc)
    end_date = datetime.utcnow()
    date_query = EventTimestamp.in_range(start_date.timestamp(), end_date.timestamp())
    query = FileEventQuery.all(date_query)
    response = connection.securitydata.search_file_events(query)
    assert response.status_code == 200


def test_stream_file_by_md5(connection):
    with pytest.raises(Py42Error):
        response = connection.securitydata.stream_file_by_md5(md5_hash)
        for _ in response:
            break


def test_stream_file_by_sha256(connection):
    with pytest.raises(Py42Error):
        response = connection.securitydata.stream_file_by_sha256(sha256_hash)
        for _ in response:
            break
