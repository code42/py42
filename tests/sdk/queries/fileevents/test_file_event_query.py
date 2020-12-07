from py42._compat import str
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery


JSON_QUERY_BASE = u'{{"groupClause":"{0}", "groups":[{1}], "srtDir":"{4}", "srtKey":"{5}", "pgNum":{2}, "pgSize":{3}}}'


def build_query_json(group_clause, group_list):
    return JSON_QUERY_BASE.format(group_clause, group_list, 1, 10000, "asc", "eventId")


def test_file_event_query_repr_does_not_throw_type_error():
    # On python 2, `repr` doesn't throw.
    # On python 3, if `repr` doesn't return type `str`, then an exception is thrown.
    try:
        _ = repr(FileEventQuery())
    except TypeError:
        raise AssertionError()


def test_file_event_query_constructs_successfully(event_filter_group):
    assert FileEventQuery(event_filter_group)


def test_file_event_query_str_with_single_filter_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group)
    json_query_str = build_query_json("AND", event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_unicode_with_single_filter_gives_correct_json_representation(
    unicode_event_filter_group,
):
    file_event_query = FileEventQuery(unicode_event_filter_group)
    json_query_str = build_query_json("AND", unicode_event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_single_filter_and_specified_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group, group_clause="AND")
    json_query_str = build_query_json("AND", event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_single_filter_or_specified_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group, group_clause="OR")
    json_query_str = build_query_json("OR", event_filter_group)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_many_filters_gives_correct_json_representation(
    event_filter_group_list,
):
    file_event_query = FileEventQuery(event_filter_group_list)
    json_query_str = build_query_json("AND", event_filter_group_list)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_many_filters_and_specified_gives_correct_json_representation(
    event_filter_group_list,
):
    file_event_query = FileEventQuery(event_filter_group_list, group_clause="AND")
    json_query_str = build_query_json("AND", event_filter_group_list)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_many_filters_or_specified_gives_correct_json_representation(
    event_filter_group_list,
):
    file_event_query = FileEventQuery(event_filter_group_list, group_clause="OR")
    json_query_str = build_query_json("OR", event_filter_group_list)
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_page_num_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.page_number = 5
    json_query_str = JSON_QUERY_BASE.format(
        "AND", event_filter_group, 5, 10000, "asc", "eventId"
    )
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_page_size_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.page_size = 500
    json_query_str = JSON_QUERY_BASE.format(
        "AND", event_filter_group, 1, 500, "asc", "eventId"
    )
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_sort_direction_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.sort_direction = "desc"
    json_query_str = JSON_QUERY_BASE.format(
        "AND", event_filter_group, 1, 10000, "desc", "eventId"
    )
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_sort_key_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.sort_key = "some_field_to_sort_by"
    json_query_str = JSON_QUERY_BASE.format(
        "AND", event_filter_group, 1, 10000, "asc", "some_field_to_sort_by"
    )
    assert str(file_event_query) == json_query_str


def test_file_event_query_from_dict_gives_correct_json_representation():
    group = {
        "filterClause": "AND",
        "filters": [{"operator": "IS", "term": "testterm", "value": "testval"}],
    }
    group_str = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"testterm", "value":"testval"}]}'
    file_event_query_dict = {"groupClause": "AND", "groups": [group]}
    file_event_query = FileEventQuery.from_dict(file_event_query_dict)
    json_query_str = JSON_QUERY_BASE.format(
        "AND", group_str, 1, 10000, "asc", "eventId"
    )
    assert str(file_event_query) == json_query_str


def test_file_event_query_dict_gives_expected_dict_representation(event_filter_group):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query_dict = dict(file_event_query)
    assert file_event_query_dict["groupClause"] == "AND"
    assert file_event_query_dict["pgNum"] == 1
    assert file_event_query_dict["pgSize"] == 10000
    assert file_event_query_dict["srtDir"] == "asc"
    assert file_event_query_dict["srtKey"] == "eventId"
    assert type(file_event_query_dict["groups"]) == list


def test_file_event_str_gives_correct_json_representation_when_pg_token_is_set(
    event_filter_group,
):
    query = FileEventQuery()
    assert query.page_token is None
    assert (
        str(query)
        == u'{"groupClause":"AND", "groups":[], "srtDir":"asc", "srtKey":"eventId", "pgNum":1, "pgSize":10000}'
    )
    query.page_token = "abc"
    assert (
        str(query)
        == u'{"groupClause":"AND", "groups":[], "srtDir":"asc", "srtKey":"eventId", "pgToken":"abc", "pgSize":10000}'
    )
