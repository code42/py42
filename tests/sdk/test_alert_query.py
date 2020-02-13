# -*- coding: utf-8 -*-

from py42._internal.compat import str
from py42.sdk.alert_query import AlertQuery

_TENANT_ID = u"tenant-id"
JSON_QUERY_BASE = u'{{"tenantId":"{0}", "groupClause":"{1}", "groups":[{2}], "pgNum":{3}, "pgSize":{4}, "srtDir":"{5}", "srtKey":"{6}"}}'


def build_query_json(group_clause, group_list):
    return JSON_QUERY_BASE.format(_TENANT_ID, group_clause, group_list, 0, 100, "asc", "CreatedAt")


def test_alert_query_repr_does_not_throw_type_error():
    # On python 2, `repr` doesn't throw.
    # On python 3, if `repr` doesn't return type `str`, then an exception is thrown.
    try:
        _ = repr(AlertQuery(_TENANT_ID))
    except TypeError:
        assert False


def test_alert_query_constructs_successfully(event_filter_group):
    assert AlertQuery(event_filter_group)


def test_alert_query_str_with_single_filter_gives_correct_json_representation(
    event_filter_group,
):
    alert_query = AlertQuery(_TENANT_ID, event_filter_group)
    json_query_str = build_query_json("AND", event_filter_group)
    assert str(alert_query) == json_query_str
