from py42.sdk.queries.fileevents.filters.cloud_query import (
    Actor,
    DirectoryID,
    Shared,
    SharedWith,
    SharingTypeAdded,
)
from ..conftest import EXISTS, IS, IS_IN, IS_NOT, NOT_EXISTS, NOT_IN


def test_actor_exists_str_gives_correct_json_representation():
    _filter = Actor.exists()
    expected = EXISTS.format("actor")
    assert str(_filter) == expected


def test_actor_not_exists_str_gives_correct_json_representation():
    _filter = Actor.not_exists()
    expected = NOT_EXISTS.format("actor")
    assert str(_filter) == expected


def test_actor_eq_str_gives_correct_json_representation():
    _filter = Actor.eq("test_actor")
    expected = IS.format("actor", "test_actor")
    assert str(_filter) == expected


def test_actor_not_eq_str_gives_correct_json_representation():
    _filter = Actor.not_eq("test_actor")
    expected = IS_NOT.format("actor", "test_actor")
    assert str(_filter) == expected


def test_actor_is_in_str_gives_correct_json_representation():
    items = ["actor1", "actor2", "actor3"]
    _filter = Actor.is_in(items)
    expected = IS_IN.format("actor", *items)
    assert str(_filter) == expected


def test_actor_not_in_str_gives_correct_json_representation():
    items = ["actor1", "actor2", "actor3"]
    _filter = Actor.not_in(items)
    expected = NOT_IN.format("actor", *items)
    assert str(_filter) == expected


def test_directory_id_eq_str_gives_correct_json_representation():
    _filter = DirectoryID.eq("test_id")
    expected = IS.format("directoryId", "test_id")
    assert str(_filter) == expected


def test_directory_id_not_eq_str_gives_correct_json_representation():
    _filter = DirectoryID.not_eq("test_id")
    expected = IS_NOT.format("directoryId", "test_id")
    assert str(_filter) == expected


def test_directory_id_is_in_str_gives_correct_json_representation():
    items = ["directoryId1", "directoryId2", "directoryId3"]
    _filter = DirectoryID.is_in(items)
    expected = IS_IN.format("directoryId", *items)
    assert str(_filter) == expected


def test_directory_id_not_in_str_gives_correct_json_representation():
    items = ["directoryId1", "directoryId2", "directoryId3"]
    _filter = DirectoryID.not_in(items)
    expected = NOT_IN.format("directoryId", *items)
    assert str(_filter) == expected


def test_shared_is_true_str_gives_correct_json_representation():
    _filter = Shared.is_true()
    expected = IS.format("shared", "TRUE")
    assert str(_filter) == expected


def test_shared_is_false_str_gives_correct_json_representation():
    _filter = Shared.is_false()
    expected = IS.format("shared", "FALSE")
    assert str(_filter) == expected


def test_shared_with_exists_str_gives_correct_json_representation():
    _filter = SharedWith.exists()
    expected = EXISTS.format("sharedWith")
    assert str(_filter) == expected


def test_shared_with_not_exists_str_gives_correct_json_representation():
    _filter = SharedWith.not_exists()
    expected = NOT_EXISTS.format("sharedWith")
    assert str(_filter) == expected


def test_shared_with_eq_str_gives_correct_json_representation():
    _filter = SharedWith.eq("test_user")
    expected = IS.format("sharedWith", "test_user")
    assert str(_filter) == expected


def test_shared_with_not_eq_str_gives_correct_json_representation():
    _filter = SharedWith.not_eq("test_user")
    expected = IS_NOT.format("sharedWith", "test_user")
    assert str(_filter) == expected


def test_shared_with_is_in_str_gives_correct_json_representation():
    items = ["user1", "user2", "user3"]
    _filter = SharedWith.is_in(items)
    expected = IS_IN.format("sharedWith", *items)
    assert str(_filter) == expected


def test_shared_with_not_in_str_gives_correct_json_representation():
    items = ["user1", "user2", "user3"]
    _filter = SharedWith.not_in(items)
    expected = NOT_IN.format("sharedWith", *items)
    assert str(_filter) == expected


def test_sharing_type_added_exists_str_gives_correct_json_representation():
    _filter = SharingTypeAdded.exists()
    expected = EXISTS.format("sharingTypeAdded")
    assert str(_filter) == expected


def test_sharing_type_added_not_exists_str_gives_correct_json_representation():
    _filter = SharingTypeAdded.not_exists()
    expected = NOT_EXISTS.format("sharingTypeAdded")
    assert str(_filter) == expected


def test_sharing_type_added_eq_str_gives_correct_json_representation():
    _filter = SharingTypeAdded.eq("test_cloud")
    expected = IS.format("sharingTypeAdded", "test_cloud")
    assert str(_filter) == expected


def test_sharing_type_added_not_eq_str_gives_correct_json_representation():
    _filter = SharingTypeAdded.not_eq("test_cloud")
    expected = IS_NOT.format("sharingTypeAdded", "test_cloud")
    assert str(_filter) == expected


def test_sharing_type_added_is_in_str_gives_correct_json_representation():
    items = ["cloud1", "cloud2", "cloud3"]
    _filter = SharingTypeAdded.is_in(items)
    expected = IS_IN.format("sharingTypeAdded", *items)
    assert str(_filter) == expected


def test_sharing_type_added_not_in_str_gives_correct_json_representation():
    items = ["cloud1", "cloud2", "cloud3"]
    _filter = SharingTypeAdded.not_in(items)
    expected = NOT_IN.format("sharingTypeAdded", *items)
    assert str(_filter) == expected
