from py42._internal.compat import str
from py42.sdk.queries.fileevents.file_event_query import FileEventQuery


JSON_QUERY_BASE = u'{{"groupClause":"{0}", "groups":[{1}], "pgNum":{2}, "pgSize":{3}, "srtDir":"{4}", "srtKey":"{5}"}}'


def build_query_json(group_clause, group_list):
    return JSON_QUERY_BASE.format(group_clause, group_list, 1, 10000, "asc", "eventId")


def test_file_event_query_repr_does_not_throw_type_error():
    # On python 2, `repr` doesn't throw.
    # On python 3, if `repr` doesn't return type `str`, then an exception is thrown.
    try:
        _ = repr(FileEventQuery())
    except TypeError:
        assert False


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


def test_file_event_query_str_with_page_num_gives_correct_json_representation(event_filter_group):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.page_number = 5
    json_query_str = JSON_QUERY_BASE.format("AND", event_filter_group, 5, 10000, "asc", "eventId")
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_page_size_gives_correct_json_representation(event_filter_group):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.page_size = 500
    json_query_str = JSON_QUERY_BASE.format("AND", event_filter_group, 1, 500, "asc", "eventId")
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_sort_direction_gives_correct_json_representation(
    event_filter_group,
):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.sort_direction = "desc"
    json_query_str = JSON_QUERY_BASE.format("AND", event_filter_group, 1, 10000, "desc", "eventId")
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_sort_key_gives_correct_json_representation(event_filter_group):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.sort_key = "some_field_to_sort_by"
    json_query_str = JSON_QUERY_BASE.format(
        "AND", event_filter_group, 1, 10000, "asc", "some_field_to_sort_by"
    )
    assert str(file_event_query) == json_query_str
