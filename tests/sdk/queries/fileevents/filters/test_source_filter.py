from tests.sdk.queries.conftest import EXISTS
from tests.sdk.queries.conftest import IS
from tests.sdk.queries.conftest import IS_IN
from tests.sdk.queries.conftest import IS_NOT
from tests.sdk.queries.conftest import NOT_EXISTS
from tests.sdk.queries.conftest import NOT_IN

from py42.sdk.queries.fileevents.filters.source_filter import SourceCategory
from py42.sdk.queries.fileevents.filters.source_filter import SourceName
from py42.sdk.queries.fileevents.filters.source_filter import SourceTabTitles
from py42.sdk.queries.fileevents.filters.source_filter import SourceTabUrls


def test_source_category_exists_str_gives_correct_json_representation():
    _filter = SourceCategory.exists()
    expected = EXISTS.format("sourceCategory")
    assert str(_filter) == expected


def test_source_category_not_exists_str_gives_correct_json_representation():
    _filter = SourceCategory.not_exists()
    expected = NOT_EXISTS.format("sourceCategory")
    assert str(_filter) == expected


def test_source_category_eq_str_gives_correct_json_representation():
    _filter = SourceCategory.eq("test_sourceCategory")
    expected = IS.format("sourceCategory", "test_sourceCategory")
    assert str(_filter) == expected


def test_source_category_not_eq_str_gives_correct_json_representation():
    _filter = SourceCategory.not_eq("test_sourceCategory")
    expected = IS_NOT.format("sourceCategory", "test_sourceCategory")
    assert str(_filter) == expected


def test_source_category_is_in_str_gives_correct_json_representation():
    items = ["test_sourceCategory_1", "test_sourceCategory_2", "test_sourceCategory_3"]
    _filter = SourceCategory.is_in(items)
    expected = IS_IN.format("sourceCategory", *sorted(items))
    assert str(_filter) == expected


def test_source_category_not_in_str_gives_correct_json_representation():
    items = ["test_sourceCategory_1", "test_sourceCategory_2", "test_sourceCategory_3"]
    _filter = SourceCategory.not_in(items)
    expected = NOT_IN.format("sourceCategory", *sorted(items))
    assert str(_filter) == expected


def test_source_name_exists_str_gives_correct_json_representation():
    _filter = SourceName.exists()
    expected = EXISTS.format("sourceName")
    assert str(_filter) == expected


def test_source_name_not_exists_str_gives_correct_json_representation():
    _filter = SourceName.not_exists()
    expected = NOT_EXISTS.format("sourceName")
    assert str(_filter) == expected


def test_source_name_eq_str_gives_correct_json_representation():
    _filter = SourceName.eq("test_sourceName")
    expected = IS.format("sourceName", "test_sourceName")
    assert str(_filter) == expected


def test_source_name_not_eq_str_gives_correct_json_representation():
    _filter = SourceName.not_eq("test_sourceName")
    expected = IS_NOT.format("sourceName", "test_sourceName")
    assert str(_filter) == expected


def test_source_name_is_in_str_gives_correct_json_representation():
    items = ["test_sourceName_1", "test_sourceName_2", "test_sourceName_3"]
    _filter = SourceName.is_in(items)
    expected = IS_IN.format("sourceName", *sorted(items))
    assert str(_filter) == expected


def test_source_name_not_in_str_gives_correct_json_representation():
    items = ["test_sourceName_1", "test_sourceName_2", "test_sourceName_3"]
    _filter = SourceName.not_in(items)
    expected = NOT_IN.format("sourceName", *sorted(items))
    assert str(_filter) == expected


def test_source_tab_titles_exists_str_gives_correct_json_representation():
    _filter = SourceTabTitles.exists()
    expected = EXISTS.format("sourceTabTitles")
    assert str(_filter) == expected


def test_source_tab_titles_not_exists_str_gives_correct_json_representation():
    _filter = SourceTabTitles.not_exists()
    expected = NOT_EXISTS.format("sourceTabTitles")
    assert str(_filter) == expected


def test_source_tab_titles_eq_str_gives_correct_json_representation():
    _filter = SourceTabTitles.eq("test_sourceTabTitles")
    expected = IS.format("sourceTabTitles", "test_sourceTabTitles")
    assert str(_filter) == expected


def test_source_tab_titles_not_eq_str_gives_correct_json_representation():
    _filter = SourceTabTitles.not_eq("test_sourceTabTitles")
    expected = IS_NOT.format("sourceTabTitles", "test_sourceTabTitles")
    assert str(_filter) == expected


def test_source_tab_titles_is_in_str_gives_correct_json_representation():
    items = [
        "test_sourceTabTitles_1",
        "test_sourceTabTitles_2",
        "test_sourceTabTitles_3",
    ]
    _filter = SourceTabTitles.is_in(items)
    expected = IS_IN.format("sourceTabTitles", *sorted(items))
    assert str(_filter) == expected


def test_source_tab_titles_not_in_str_gives_correct_json_representation():
    items = [
        "test_sourceTabTitles_1",
        "test_sourceTabTitles_2",
        "test_sourceTabTitles_3",
    ]
    _filter = SourceTabTitles.not_in(items)
    expected = NOT_IN.format("sourceTabTitles", *sorted(items))
    assert str(_filter) == expected


def test_source_tab_urls_exists_str_gives_correct_json_representation():
    _filter = SourceTabUrls.exists()
    expected = EXISTS.format("sourceTabUrls")
    assert str(_filter) == expected


def test_source_tab_urls_not_exists_str_gives_correct_json_representation():
    _filter = SourceTabUrls.not_exists()
    expected = NOT_EXISTS.format("sourceTabUrls")
    assert str(_filter) == expected


def test_source_tab_urls_eq_str_gives_correct_json_representation():
    _filter = SourceTabUrls.eq("test_sourceTabUrls")
    expected = IS.format("sourceTabUrls", "test_sourceTabUrls")
    assert str(_filter) == expected


def test_source_tab_urls_not_eq_str_gives_correct_json_representation():
    _filter = SourceTabUrls.not_eq("test_sourceTabUrls")
    expected = IS_NOT.format("sourceTabUrls", "test_sourceTabUrls")
    assert str(_filter) == expected


def test_source_tab_urls_is_in_str_gives_correct_json_representation():
    items = ["test_sourceTabUrls_1", "test_sourceTabUrls_2", "test_sourceTabUrls_3"]
    _filter = SourceTabUrls.is_in(items)
    expected = IS_IN.format("sourceTabUrls", *sorted(items))
    assert str(_filter) == expected


def test_source_tab_urls_not_in_str_gives_correct_json_representation():
    items = ["test_sourceTabUrls_1", "test_sourceTabUrls_2", "test_sourceTabUrls_3"]
    _filter = SourceTabUrls.not_in(items)
    expected = NOT_IN.format("sourceTabUrls", *sorted(items))
    assert str(_filter) == expected
