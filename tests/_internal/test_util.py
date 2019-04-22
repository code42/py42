import os

import pytest

import py42.util as util

TEST_FILENAME = "file.txt"
TEST_DIR = "/Users/john.doe"
TEST_PATH = "{0}/{1}".format(TEST_DIR, TEST_FILENAME)


def mock_access(can_access=True):
    def access(path, int):
        return can_access
    return access


def mock_dir_only_access():
    def access(path, int):
        return path == TEST_DIR and int == os.W_OK
    return access


@pytest.fixture
def non_existing_dir(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda(path): False)
    monkeypatch.setattr("os.access", mock_access(False))
    return TEST_PATH


@pytest.fixture
def existing_dir_not_writeable(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda(path): path == TEST_DIR)
    monkeypatch.setattr("os.access", mock_access(False))
    return TEST_PATH


@pytest.fixture
def non_existing_file_writeable(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda(path): path == TEST_DIR)
    monkeypatch.setattr("os.access", mock_access())
    return TEST_PATH


@pytest.fixture
def existing_file_writeable(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda(path): True)
    monkeypatch.setattr("os.access", mock_access())
    return TEST_PATH


@pytest.fixture
def existing_file_not_writeable(monkeypatch):
    monkeypatch.setattr("posixpath.exists", lambda(path): True)
    monkeypatch.setattr("os.access", mock_dir_only_access())
    return TEST_PATH


def test_verify_write_permissions_if_dir_not_exists_raises_io_error(non_existing_dir):
    with pytest.raises(Exception) as e:
        util.verify_path_writeable(non_existing_dir)
    assert e.type == IOError
    assert e.value.args[0] == "Directory does not exist: {0}".format(TEST_DIR)


def test_verify_write_permissions_if_dir_not_writeable_raises_io_error(existing_dir_not_writeable):
    with pytest.raises(Exception) as e:
        util.verify_path_writeable(existing_dir_not_writeable)
    assert e.type == IOError
    assert e.value.args[0] == "Insufficient permissions to write to directory: {0}".format(TEST_DIR)


def test_verify_write_permissions_if_file_not_writeable_raises_io_error(existing_file_not_writeable):
    with pytest.raises(Exception) as e:
        util.verify_path_writeable(existing_file_not_writeable)
    assert e.type == IOError
    assert e.value.args[0] == "Insufficient permissions to write to file: {0}".format(existing_file_not_writeable)


def test_verify_write_permissions_when_existing_file_writeable_returns_path(existing_file_writeable):
    path = util.verify_path_writeable(existing_file_writeable)
    assert path == existing_file_writeable


def test_verify_write_permissions_when_non_existing_file_writeable_returns_path(non_existing_file_writeable):
    path = util.verify_path_writeable(non_existing_file_writeable)
    assert path == non_existing_file_writeable


def test_build_path_with_filename_returns_path_with_curdir():
    path = util.build_path(TEST_FILENAME)
    assert path == "./{0}".format(TEST_FILENAME)


def test_build_path_with_filename_and_save_as_dir_returns_path_with_save_as_dir():
    path = util.build_path(TEST_FILENAME, directory=TEST_DIR)
    assert path == "{0}/{1}".format(TEST_DIR, TEST_FILENAME)


def test_build_path_with_filename_and_none_save_as_dir_returns_path_with_curdir():
    path = util.build_path(TEST_FILENAME, directory=None)
    assert path == "./{0}".format(TEST_FILENAME)


def test_build_path_with_filename_none_save_as_dir_and_custom_default_dir_returns_path_with_default_dir():
    path = util.build_path(TEST_FILENAME, directory=None, default_dir="/temp")
    assert path == "/temp/{0}".format(TEST_FILENAME)
