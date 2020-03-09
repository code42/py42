from py42.sdk.queries.fileevents.filters.file_filter import (
    FileCategory,
    FileName,
    FileOwner,
    FilePath,
    MD5,
    SHA256,
)
from ..conftest import EXISTS, IS, IS_IN, IS_NOT, NOT_EXISTS, NOT_IN


def test_file_category_eq_str_gives_correct_json_representation():
    _filter = FileCategory.eq("test_category")
    expected = IS.format("fileCategory", "test_category")
    assert str(_filter) == expected


def test_file_category_not_eq_str_gives_correct_json_representation():
    _filter = FileCategory.not_eq("test_category")
    expected = IS_NOT.format("fileCategory", "test_category")
    assert str(_filter) == expected


def test_file_category_is_in_str_gives_correct_json_representation():
    items = ["category1", "category2", "category3"]
    _filter = FileCategory.is_in(items)
    expected = IS_IN.format("fileCategory", *items)
    assert str(_filter) == expected


def test_file_category_not_in_str_gives_correct_json_representation():
    items = ["category1", "category2", "category3"]
    _filter = FileCategory.not_in(items)
    expected = NOT_IN.format("fileCategory", *items)
    assert str(_filter) == expected


def test_file_name_exists_str_gives_correct_json_representation():
    _filter = FileName.exists()
    expected = EXISTS.format("fileName")
    assert str(_filter) == expected


def test_file_name_not_exists_str_gives_correct_json_representation():
    _filter = FileName.not_exists()
    expected = NOT_EXISTS.format("fileName")
    assert str(_filter) == expected


def test_file_name_eq_str_gives_correct_json_representation():
    _filter = FileName.eq("test_fileName")
    expected = IS.format("fileName", "test_fileName")
    assert str(_filter) == expected


def test_file_name_not_eq_str_gives_correct_json_representation():
    _filter = FileName.not_eq("test_fileName")
    expected = IS_NOT.format("fileName", "test_fileName")
    assert str(_filter) == expected


def test_file_name_is_in_str_gives_correct_json_representation():
    items = ["fileName", "fileName", "fileName"]
    _filter = FileName.is_in(items)
    expected = IS_IN.format("fileName", *items)
    assert str(_filter) == expected


def test_file_name_not_in_str_gives_correct_json_representation():
    items = ["fileName1", "fileName2", "fileName3"]
    _filter = FileName.not_in(items)
    expected = NOT_IN.format("fileName", *items)
    assert str(_filter) == expected


def test_file_owner_exists_str_gives_correct_json_representation():
    _filter = FileOwner.exists()
    expected = EXISTS.format("fileOwner")
    assert str(_filter) == expected


def test_file_owner_not_exists_str_gives_correct_json_representation():
    _filter = FileOwner.not_exists()
    expected = NOT_EXISTS.format("fileOwner")
    assert str(_filter) == expected


def test_file_owner_eq_str_gives_correct_json_representation():
    _filter = FileOwner.eq("test_fileName")
    expected = IS.format("fileOwner", "test_fileName")
    assert str(_filter) == expected


def test_file_owner_not_eq_str_gives_correct_json_representation():
    _filter = FileOwner.not_eq("test_fileName")
    expected = IS_NOT.format("fileOwner", "test_fileName")
    assert str(_filter) == expected


def test_file_owner_is_in_str_gives_correct_json_representation():
    items = ["fileOwner1", "fileOwner2", "fileOwner3"]
    _filter = FileOwner.is_in(items)
    expected = IS_IN.format("fileOwner", *items)
    assert str(_filter) == expected


def test_file_owner_not_in_str_gives_correct_json_representation():
    items = ["fileOwner1", "fileOwner2", "fileOwner3"]
    _filter = FileOwner.not_in(items)
    expected = NOT_IN.format("fileOwner", *items)
    assert str(_filter) == expected


def test_file_path_exists_str_gives_correct_json_representation():
    _filter = FilePath.exists()
    expected = EXISTS.format("filePath")
    assert str(_filter) == expected


def test_file_path_not_exists_str_gives_correct_json_representation():
    _filter = FilePath.not_exists()
    expected = NOT_EXISTS.format("filePath")
    assert str(_filter) == expected


def test_file_path_eq_str_gives_correct_json_representation():
    _filter = FilePath.eq("test_filePath")
    expected = IS.format("filePath", "test_filePath")
    assert str(_filter) == expected


def test_file_path_not_eq_str_gives_correct_json_representation():
    _filter = FilePath.not_eq("test_filePath")
    expected = IS_NOT.format("filePath", "test_filePath")
    assert str(_filter) == expected


def test_file_path_is_in_str_gives_correct_json_representation():
    items = ["filePath1", "filePath2", "filePath3"]
    _filter = FilePath.is_in(items)
    expected = IS_IN.format("filePath", *items)
    assert str(_filter) == expected


def test_file_path_not_in_str_gives_correct_json_representation():
    items = ["filePath1", "filePath2", "filePath3"]
    _filter = FilePath.not_in(items)
    expected = NOT_IN.format("filePath", *items)
    assert str(_filter) == expected


def test_md5_exists_str_gives_correct_json_representation():
    _filter = MD5.exists()
    expected = EXISTS.format("md5Checksum")
    assert str(_filter) == expected


def test_md5_not_exists_str_gives_correct_json_representation():
    _filter = MD5.not_exists()
    expected = NOT_EXISTS.format("md5Checksum")
    assert str(_filter) == expected


def test_md5_eq_str_gives_correct_json_representation():
    _filter = MD5.eq("test_md5")
    expected = IS.format("md5Checksum", "test_md5")
    assert str(_filter) == expected


def test_md5_not_eq_str_gives_correct_json_representation():
    _filter = MD5.not_eq("test_md5")
    expected = IS_NOT.format("md5Checksum", "test_md5")
    assert str(_filter) == expected


def test_md5_is_in_str_gives_correct_json_representation():
    items = ["md51", "md52", "md53"]
    _filter = MD5.is_in(items)
    expected = IS_IN.format("md5Checksum", *items)
    assert str(_filter) == expected


def test_md5_not_in_str_gives_correct_json_representation():
    items = ["md51", "md52", "md53"]
    _filter = MD5.not_in(items)
    expected = NOT_IN.format("md5Checksum", *items)
    assert str(_filter) == expected


def test_sha256_exists_str_gives_correct_json_representation():
    _filter = SHA256.exists()
    expected = EXISTS.format("sha256Checksum")
    assert str(_filter) == expected


def test_sha256_not_exists_str_gives_correct_json_representation():
    _filter = SHA256.not_exists()
    expected = NOT_EXISTS.format("sha256Checksum")
    assert str(_filter) == expected


def test_sha256_eq_str_gives_correct_json_representation():
    _filter = SHA256.eq("test_sha256")
    expected = IS.format("sha256Checksum", "test_sha256")
    assert str(_filter) == expected


def test_sha256_not_eq_str_gives_correct_json_representation():
    _filter = SHA256.not_eq("test_sha256")
    expected = IS_NOT.format("sha256Checksum", "test_sha256")
    assert str(_filter) == expected


def test_sha256_is_in_str_gives_correct_json_representation():
    items = ["sha2561", "sha2562", "sha2563"]
    _filter = SHA256.is_in(items)
    expected = IS_IN.format("sha256Checksum", *items)
    assert str(_filter) == expected


def test_sha256_not_in_str_gives_correct_json_representation():
    items = ["sha2561", "sha2562", "sha2563"]
    _filter = SHA256.not_in(items)
    expected = NOT_IN.format("sha256Checksum", *items)
    assert str(_filter) == expected
