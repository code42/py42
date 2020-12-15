from datetime import datetime
from datetime import timezone

from py42.clients.securitydata import PlanStorageInfo
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery
from py42.sdk.queries.fileevents.filters import EventTimestamp


def test_get_all_plan_security_events(connection):
    response = connection.securitydata.get_all_plan_security_events()


def test_get_all_user_security_events():
    pass


def test_search_file_events(connection):

    start_date = datetime(2020, 9, 13, tzinfo=timezone.utc)
    end_date = datetime.utcnow()
    date_query = EventTimestamp.in_range(start_date.timestamp(), end_date.timestamp())
    query = FileEventQuery.all(date_query)
    response = connection.securitydata.search_file_events(query)
    assert response.status_code == 200


def test_get_security_plan_storage_info_list():
    pass


def test_stream_file_by_md5():
    pass


def test_stream_file_by_sha256():
    pass
