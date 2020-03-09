from py42.sdk.queries.fileevents.filters.exposure_filter import (
    ExposureType,
    ProcessName,
    ProcessOwner,
    RemovableMediaName,
    SyncDestination,
    TabURL,
    WindowTitle,
)
from tests.sdk.queries.conftest import EXISTS, IS, IS_IN, IS_NOT, NOT_EXISTS, NOT_IN


def test_exposure_type_exists_str_gives_correct_json_representation():
    _filter = ExposureType.exists()
    expected = EXISTS.format("exposure")
    assert str(_filter) == expected


def test_exposure_type_not_exists_str_gives_correct_json_representation():
    _filter = ExposureType.not_exists()
    expected = NOT_EXISTS.format("exposure")
    assert str(_filter) == expected


def test_exposure_type_eq_str_gives_correct_json_representation():
    _filter = ExposureType.eq("test_exposure")
    expected = IS.format("exposure", "test_exposure")
    assert str(_filter) == expected


def test_exposure_type_not_eq_str_gives_correct_json_representation():
    _filter = ExposureType.not_eq("test_exposure")
    expected = IS_NOT.format("exposure", "test_exposure")
    assert str(_filter) == expected


def test_exposure_type_is_in_str_gives_correct_json_representation():
    items = ["exposure1", "exposure2", "exposure3"]
    _filter = ExposureType.is_in(items)
    expected = IS_IN.format("exposure", *items)
    assert str(_filter) == expected


def test_exposure_type_not_in_str_gives_correct_json_representation():
    items = ["exposure1", "exposure2", "exposure3"]
    _filter = ExposureType.not_in(items)
    expected = NOT_IN.format("exposure", *items)
    assert str(_filter) == expected


def test_process_name_exists_str_gives_correct_json_representation():
    _filter = ProcessName.exists()
    expected = EXISTS.format("processName")
    assert str(_filter) == expected


def test_process_name_not_exists_str_gives_correct_json_representation():
    _filter = ProcessName.not_exists()
    expected = NOT_EXISTS.format("processName")
    assert str(_filter) == expected


def test_process_name_eq_str_gives_correct_json_representation():
    _filter = ProcessName.eq("test_name")
    expected = IS.format("processName", "test_name")
    assert str(_filter) == expected


def test_process_name_not_eq_str_gives_correct_json_representation():
    _filter = ProcessName.not_eq("test_name")
    expected = IS_NOT.format("processName", "test_name")
    assert str(_filter) == expected


def test_process_name_is_in_str_gives_correct_json_representation():
    items = ["n1", "n2", "n3"]
    _filter = ProcessName.is_in(items)
    expected = IS_IN.format("processName", *items)
    assert str(_filter) == expected


def test_process_name_not_in_str_gives_correct_json_representation():
    items = ["n1", "n2", "n3"]
    _filter = ProcessName.not_in(items)
    expected = NOT_IN.format("processName", *items)
    assert str(_filter) == expected


def test_process_owner_exists_str_gives_correct_json_representation():
    _filter = ProcessOwner.exists()
    expected = EXISTS.format("processOwner")
    assert str(_filter) == expected


def test_process_owner_not_exists_str_gives_correct_json_representation():
    _filter = ProcessOwner.not_exists()
    expected = NOT_EXISTS.format("processOwner")
    assert str(_filter) == expected


def test_process_owner_eq_str_gives_correct_json_representation():
    _filter = ProcessOwner.eq("test_owner")
    expected = IS.format("processOwner", "test_owner")
    assert str(_filter) == expected


def test_process_owner_not_eq_str_gives_correct_json_representation():
    _filter = ProcessOwner.not_eq("test_owner")
    expected = IS_NOT.format("processOwner", "test_owner")
    assert str(_filter) == expected


def test_process_owner_is_in_str_gives_correct_json_representation():
    items = ["owner1", "owner2", "owner3"]
    _filter = ProcessOwner.is_in(items)
    expected = IS_IN.format("processOwner", *items)
    assert str(_filter) == expected


def test_process_owner_not_in_str_gives_correct_json_representation():
    items = ["owner1", "owner2", "owner3"]
    _filter = ProcessOwner.not_in(items)
    expected = NOT_IN.format("processOwner", *items)
    assert str(_filter) == expected


def test_removable_media_name_exists_str_gives_correct_json_representation():
    _filter = RemovableMediaName.exists()
    expected = EXISTS.format("removableMediaName")
    assert str(_filter) == expected


def test_removable_media_name_not_exists_str_gives_correct_json_representation():
    _filter = RemovableMediaName.not_exists()
    expected = NOT_EXISTS.format("removableMediaName")
    assert str(_filter) == expected


def test_removable_media_name_eq_str_gives_correct_json_representation():
    _filter = RemovableMediaName.eq("test_name")
    expected = IS.format("removableMediaName", "test_name")
    assert str(_filter) == expected


def test_removable_media_name_not_eq_str_gives_correct_json_representation():
    _filter = RemovableMediaName.not_eq("test_name")
    expected = IS_NOT.format("removableMediaName", "test_name")
    assert str(_filter) == expected


def test_removable_media_name_is_in_str_gives_correct_json_representation():
    items = ["name1", "name2", "name3"]
    _filter = RemovableMediaName.is_in(items)
    expected = IS_IN.format("removableMediaName", *items)
    assert str(_filter) == expected


def test_removable_media_name_not_in_str_gives_correct_json_representation():
    items = ["name1", "name2", "name3"]
    _filter = RemovableMediaName.not_in(items)
    expected = NOT_IN.format("removableMediaName", *items)
    assert str(_filter) == expected


def test_sync_destination_name_exists_str_gives_correct_json_representation():
    _filter = SyncDestination.exists()
    expected = EXISTS.format("syncDestination")
    assert str(_filter) == expected


def test_sync_destination_name_not_exists_str_gives_correct_json_representation():
    _filter = SyncDestination.not_exists()
    expected = NOT_EXISTS.format("syncDestination")
    assert str(_filter) == expected


def test_sync_destination_name_eq_str_gives_correct_json_representation():
    _filter = SyncDestination.eq("test_dest")
    expected = IS.format("syncDestination", "test_dest")
    assert str(_filter) == expected


def test_sync_destination_name_not_eq_str_gives_correct_json_representation():
    _filter = SyncDestination.not_eq("test_dest")
    expected = IS_NOT.format("syncDestination", "test_dest")
    assert str(_filter) == expected


def test_sync_destination_name_is_in_str_gives_correct_json_representation():
    items = ["dest1", "dest2", "dest3"]
    _filter = SyncDestination.is_in(items)
    expected = IS_IN.format("syncDestination", *items)
    assert str(_filter) == expected


def test_sync_destination_name_not_in_str_gives_correct_json_representation():
    items = ["dest1", "dest2", "dest3"]
    _filter = SyncDestination.not_in(items)
    expected = NOT_IN.format("syncDestination", *items)
    assert str(_filter) == expected


def test_tab_url_exists_str_gives_correct_json_representation():
    _filter = TabURL.exists()
    expected = EXISTS.format("tabUrl")
    assert str(_filter) == expected


def test_tab_url_not_exists_str_gives_correct_json_representation():
    _filter = TabURL.not_exists()
    expected = NOT_EXISTS.format("tabUrl")
    assert str(_filter) == expected


def test_tab_url_eq_str_gives_correct_json_representation():
    _filter = TabURL.eq("test_tab_url")
    expected = IS.format("tabUrl", "test_tab_url")
    assert str(_filter) == expected


def test_tab_url_not_eq_str_gives_correct_json_representation():
    _filter = TabURL.not_eq("test_tab_url")
    expected = IS_NOT.format("tabUrl", "test_tab_url")
    assert str(_filter) == expected


def test_tab_url_is_in_str_gives_correct_json_representation():
    items = ["tab1", "tab2", "tab3"]
    _filter = TabURL.is_in(items)
    expected = IS_IN.format("tabUrl", *items)
    assert str(_filter) == expected


def test_tab_url_not_in_str_gives_correct_json_representation():
    items = ["tab1", "tab2", "tab3"]
    _filter = TabURL.not_in(items)
    expected = NOT_IN.format("tabUrl", *items)
    assert str(_filter) == expected


def test_window_title_exists_str_gives_correct_json_representation():
    _filter = WindowTitle.exists()
    expected = EXISTS.format("windowTitle")
    assert str(_filter) == expected


def test_window_title_not_exists_str_gives_correct_json_representation():
    _filter = WindowTitle.not_exists()
    expected = NOT_EXISTS.format("windowTitle")
    assert str(_filter) == expected


def test_window_title_eq_str_gives_correct_json_representation():
    _filter = WindowTitle.eq("test_window")
    expected = IS.format("windowTitle", "test_window")
    assert str(_filter) == expected


def test_window_title_not_eq_str_gives_correct_json_representation():
    _filter = WindowTitle.not_eq("test_window")
    expected = IS_NOT.format("windowTitle", "test_window")
    assert str(_filter) == expected


def test_window_title_is_in_str_gives_correct_json_representation():
    items = ["window1", "window2", "window3"]
    _filter = WindowTitle.is_in(items)
    expected = IS_IN.format("windowTitle", *items)
    assert str(_filter) == expected


def test_window_title_not_in_str_gives_correct_json_representation():
    items = ["window1", "window2", "window3"]
    _filter = WindowTitle.not_in(items)
    expected = NOT_IN.format("windowTitle", *items)
    assert str(_filter) == expected
