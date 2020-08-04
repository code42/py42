from datetime import datetime

import pytest
from services._connection import Connection

from py42.services.storage import StorageSecurityService

uri = u"/api/SecurityDetectionEvent"
mock_min_ts = 1000000
mock_max_ts = 2000000


@pytest.fixture
def py42session(mocker):
    return mocker.MagicMock(spec=Connection)


@pytest.fixture
def storage_security_client(py42session):
    return StorageSecurityService(py42session)


@pytest.fixture
def min_time_str():
    return get_time_str_from_timestamp(mock_min_ts)


@pytest.fixture
def max_time_str():
    return get_time_str_from_timestamp(mock_max_ts)


def get_time_str_from_timestamp(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime(u"%Y-%m-%dT%H:%M:%S.%fZ")


@pytest.fixture
def security_detection_events_params(min_time_str, max_time_str):
    return {
        u"userUid": None,
        u"planUid": None,
        u"cursor": "Cursor",
        u"incFiles": None,
        u"eventType": None,
        u"minTs": min_time_str,
        u"maxTs": max_time_str,
        u"summarize": None,
    }


@pytest.fixture
def plan_security_detection_events_params(security_detection_events_params):
    params = security_detection_events_params
    params[u"planUid"] = "PlanUid"
    params[u"incFiles"] = True
    params[u"eventType"] = "EventType"
    return params


@pytest.fixture
def user_security_detection_events_params(security_detection_events_params):
    params = security_detection_events_params
    params[u"userUid"] = "UserUid"
    params[u"incFiles"] = True
    params[u"eventType"] = "EventType"
    return params


@pytest.fixture
def security_detection_event_summary_params(security_detection_events_params):
    params = security_detection_events_params
    params[u"userUid"] = "UserUid"
    params[u"summarize"] = True
    return params


class TestStorageSecurityClient(object):
    def test_get_plan_security_events_calls_get_with_correct_params(
        self,
        storage_security_client,
        py42session,
        plan_security_detection_events_params,
    ):
        params = plan_security_detection_events_params
        storage_security_client.get_plan_security_events(
            plan_uid=params[u"planUid"],
            cursor=params[u"cursor"],
            include_files=params[u"incFiles"],
            event_types=params[u"eventType"],
            min_timestamp=mock_min_ts,
            max_timestamp=mock_max_ts,
        )
        py42session.get.assert_called_once_with(uri, params=params)

    def test_get_user_security_events_calls_get_with_correct_params(
        self,
        storage_security_client,
        py42session,
        user_security_detection_events_params,
    ):
        params = user_security_detection_events_params
        storage_security_client.get_user_security_events(
            user_uid=params[u"userUid"],
            cursor=params[u"cursor"],
            include_files=params[u"incFiles"],
            event_types=params[u"eventType"],
            min_timestamp=mock_min_ts,
            max_timestamp=mock_max_ts,
        )
        py42session.get.assert_called_once_with(uri, params=params)

    def test_get_security_detection_event_summary_calls_get_with_correct_params(
        self,
        storage_security_client,
        py42session,
        security_detection_event_summary_params,
    ):
        params = security_detection_event_summary_params
        storage_security_client.get_security_detection_event_summary(
            user_uid=params[u"userUid"],
            cursor=params[u"cursor"],
            min_timestamp=mock_min_ts,
            max_timestamp=mock_max_ts,
        )
        py42session.get.assert_called_once_with(uri, params=params)
