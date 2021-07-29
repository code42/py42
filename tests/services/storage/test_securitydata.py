from datetime import datetime

import pytest

from py42.services._connection import Connection
from py42.services.storage.securitydata import StorageSecurityDataService

uri = "/api/SecurityDetectionEvent"
mock_min_ts = 1000000
mock_max_ts = 2000000

min_ts_string_format = "1970-01-12 13:46:40"
max_ts_string_format = "1970-01-24 03:33:20"


@pytest.fixture
def py42session(mocker):
    return mocker.MagicMock(spec=Connection)


@pytest.fixture
def storage_security_service(py42session):
    return StorageSecurityDataService(py42session)


@pytest.fixture
def min_time_str():
    return get_time_str_from_timestamp(mock_min_ts)


@pytest.fixture
def max_time_str():
    return get_time_str_from_timestamp(mock_max_ts)


def get_time_str_from_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


@pytest.fixture
def security_detection_events_params(min_time_str, max_time_str):
    return {
        "userUid": None,
        "planUid": None,
        "cursor": "Cursor",
        "incFiles": None,
        "eventType": None,
        "minTs": min_time_str,
        "maxTs": max_time_str,
        "summarize": None,
    }


@pytest.fixture
def plan_security_detection_events_params(security_detection_events_params):
    params = security_detection_events_params
    params["planUid"] = "PlanUid"
    params["incFiles"] = True
    params["eventType"] = "EventType"
    return params


@pytest.fixture
def user_security_detection_events_params(security_detection_events_params):
    params = security_detection_events_params
    params["userUid"] = "UserUid"
    params["incFiles"] = True
    params["eventType"] = "EventType"
    return params


@pytest.fixture
def security_detection_event_summary_params(security_detection_events_params):
    params = security_detection_events_params
    params["userUid"] = "UserUid"
    params["summarize"] = True
    return params


class TestStorageSecurityService:
    def test_get_plan_security_events_calls_get_with_correct_params(
        self,
        storage_security_service,
        py42session,
        plan_security_detection_events_params,
    ):
        params = plan_security_detection_events_params
        storage_security_service.get_plan_security_events(
            plan_uid=params["planUid"],
            cursor=params["cursor"],
            include_files=params["incFiles"],
            event_types=params["eventType"],
            min_timestamp=datetime.utcfromtimestamp(mock_min_ts),
            max_timestamp=datetime.utcfromtimestamp(mock_max_ts),
        )
        py42session.get.assert_called_once_with(uri, params=params)

    def test_get_user_security_events_calls_get_with_correct_params(
        self,
        storage_security_service,
        py42session,
        user_security_detection_events_params,
    ):
        params = user_security_detection_events_params
        storage_security_service.get_user_security_events(
            user_uid=params["userUid"],
            cursor=params["cursor"],
            include_files=params["incFiles"],
            event_types=params["eventType"],
            min_timestamp=datetime.utcfromtimestamp(mock_min_ts),
            max_timestamp=datetime.utcfromtimestamp(mock_max_ts),
        )
        py42session.get.assert_called_once_with(uri, params=params)

    def test_get_security_detection_event_summary_calls_get_with_correct_params(
        self,
        storage_security_service,
        py42session,
        security_detection_event_summary_params,
    ):
        params = security_detection_event_summary_params
        storage_security_service.get_security_detection_event_summary(
            user_uid=params["userUid"],
            cursor=params["cursor"],
            min_timestamp=datetime.utcfromtimestamp(mock_min_ts),
            max_timestamp=datetime.utcfromtimestamp(mock_max_ts),
        )
        py42session.get.assert_called_once_with(uri, params=params)

    def test_get_security_detection_event_summary_calls_get_with_correct_date_params_for_str_format(
        self,
        storage_security_service,
        py42session,
        security_detection_event_summary_params,
    ):
        params = security_detection_event_summary_params
        storage_security_service.get_security_detection_event_summary(
            user_uid=params["userUid"],
            cursor=params["cursor"],
            min_timestamp=min_ts_string_format,
            max_timestamp=max_ts_string_format,
        )
        py42session.get.assert_called_once_with(uri, params=params)

    def test_get_security_detection_event_summary_calls_get_with_correct_date_params_for_datetime_format(
        self,
        storage_security_service,
        py42session,
        security_detection_event_summary_params,
    ):
        params = security_detection_event_summary_params
        storage_security_service.get_security_detection_event_summary(
            user_uid=params["userUid"],
            cursor=params["cursor"],
            min_timestamp=datetime.strptime(min_ts_string_format, "%Y-%m-%d %H:%M:%S"),
            max_timestamp=datetime.strptime(max_ts_string_format, "%Y-%m-%d %H:%M:%S"),
        )
        py42session.get.assert_called_once_with(uri, params=params)
