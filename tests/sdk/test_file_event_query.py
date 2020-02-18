# -*- coding: utf-8 -*-

from datetime import datetime
from time import time

from .conftest import format_timestamp, format_datetime
from py42._internal.compat import str
from py42.sdk.file_event_query import (
    DeviceUsername,
    EventTimestamp,
    EventType,
    ExposureType,
    FileEventQuery,
    FileName,
    FilePath,
    InsertionTimestamp,
    MD5,
    OSHostname,
    PrivateIPAddress,
    PublicIPAddress,
    SHA256,
)

JSON_QUERY_BASE = u'{{"groupClause":"{0}", "groups":[{1}], "pgNum":{2}, "pgSize":{3}, "srtDir":"{4}", "srtKey":"{5}"}}'


def build_query_json(group_clause, group_list):
    return JSON_QUERY_BASE.format(group_clause, group_list, 1, 100, "asc", "eventId")


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
    json_query_str = JSON_QUERY_BASE.format("AND", event_filter_group, 5, 100, "asc", "eventId")
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
    json_query_str = JSON_QUERY_BASE.format("AND", event_filter_group, 1, 100, "desc", "eventId")
    assert str(file_event_query) == json_query_str


def test_file_event_query_str_with_sort_key_gives_correct_json_representation(event_filter_group):
    file_event_query = FileEventQuery(event_filter_group)
    file_event_query.sort_key = "some_field_to_sort_by"
    json_query_str = JSON_QUERY_BASE.format(
        "AND", event_filter_group, 1, 100, "asc", "some_field_to_sort_by"
    )
    assert str(file_event_query) == json_query_str


def test_md5_exists_str_gives_correct_json_representation():
    _filter = MD5.exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"EXISTS", "term":"md5Checksum", "value":null}]}'
    assert str(_filter) == expected


def test_md5_not_exists_str_gives_correct_json_representation():
    _filter = MD5.not_exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_EXIST", "term":"md5Checksum", "value":null}]}'
    assert str(_filter) == expected


def test_md5_eq_str_gives_correct_json_representation():
    _filter = MD5.eq("test_md5")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"md5Checksum", "value":"test_md5"}]}'
    assert str(_filter) == expected


def test_md5_not_eq_str_gives_correct_json_representation():
    _filter = MD5.not_eq("test_md5")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"md5Checksum", "value":"test_md5"}]}'
    assert str(_filter) == expected


def test_md5_is_in_str_gives_correct_json_representation():
    items = ["md51", "md52", "md53"]
    _filter = MD5.is_in(items)
    expected = '{"filterClause":"OR", "filters":[{"operator":"IS", "term":"md5Checksum", "value":"md51"},{"operator":"IS", "term":"md5Checksum", "value":"md52"},{"operator":"IS", "term":"md5Checksum", "value":"md53"}]}'
    assert str(_filter) == expected


def test_md5_not_in_str_gives_correct_json_representation():
    items = ["md51", "md52", "md53"]
    _filter = MD5.not_in(items)
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"md5Checksum", "value":"md51"},{"operator":"IS_NOT", "term":"md5Checksum", "value":"md52"},{"operator":"IS_NOT", "term":"md5Checksum", "value":"md53"}]}'
    assert str(_filter) == expected


def test_sha256_exists_str_gives_correct_json_representation():
    _filter = SHA256.exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"EXISTS", "term":"sha256Checksum", "value":null}]}'
    assert str(_filter) == expected


def test_sha256_not_exists_str_gives_correct_json_representation():
    _filter = SHA256.not_exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_EXIST", "term":"sha256Checksum", "value":null}]}'
    assert str(_filter) == expected


def test_sha256_eq_str_gives_correct_json_representation():
    _filter = SHA256.eq("test_sha256")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"sha256Checksum", "value":"test_sha256"}]}'
    assert str(_filter) == expected


def test_sha256_not_eq_str_gives_correct_json_representation():
    _filter = SHA256.not_eq("test_sha256")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"sha256Checksum", "value":"test_sha256"}]}'
    assert str(_filter) == expected


def test_sha256_is_in_str_gives_correct_json_representation():
    items = ["sha2561", "sha2562", "sha2563"]
    _filter = SHA256.is_in(items)
    expected = '{"filterClause":"OR", "filters":[{"operator":"IS", "term":"sha256Checksum", "value":"sha2561"},{"operator":"IS", "term":"sha256Checksum", "value":"sha2562"},{"operator":"IS", "term":"sha256Checksum", "value":"sha2563"}]}'
    assert str(_filter) == expected


def test_sha256_not_in_str_gives_correct_json_representation():
    items = ["sha2561", "sha2562", "sha2563"]
    _filter = SHA256.not_in(items)
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"sha256Checksum", "value":"sha2561"},{"operator":"IS_NOT", "term":"sha256Checksum", "value":"sha2562"},{"operator":"IS_NOT", "term":"sha256Checksum", "value":"sha2563"}]}'
    assert str(_filter) == expected


def test_os_hostname_exists_str_gives_correct_json_representation():
    _filter = OSHostname.exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"EXISTS", "term":"osHostName", "value":null}]}'
    assert str(_filter) == expected


def test_os_hostname_not_exists_str_gives_correct_json_representation():
    _filter = OSHostname.not_exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_EXIST", "term":"osHostName", "value":null}]}'
    assert str(_filter) == expected


def test_os_hostname_eq_str_gives_correct_json_representation():
    _filter = OSHostname.eq("test_osHostName")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"osHostName", "value":"test_osHostName"}]}'
    assert str(_filter) == expected


def test_os_hostname_not_eq_str_gives_correct_json_representation():
    _filter = OSHostname.not_eq("test_osHostName")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"osHostName", "value":"test_osHostName"}]}'
    assert str(_filter) == expected


def test_os_hostname_is_in_str_gives_correct_json_representation():
    items = ["osHostName1", "osHostName2", "osHostName3"]
    _filter = OSHostname.is_in(items)
    expected = '{"filterClause":"OR", "filters":[{"operator":"IS", "term":"osHostName", "value":"osHostName1"},{"operator":"IS", "term":"osHostName", "value":"osHostName2"},{"operator":"IS", "term":"osHostName", "value":"osHostName3"}]}'
    assert str(_filter) == expected


def test_os_hostname_not_in_str_gives_correct_json_representation():
    items = ["osHostName1", "osHostName2", "osHostName3"]
    _filter = OSHostname.not_in(items)
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"osHostName", "value":"osHostName1"},{"operator":"IS_NOT", "term":"osHostName", "value":"osHostName2"},{"operator":"IS_NOT", "term":"osHostName", "value":"osHostName3"}]}'
    assert str(_filter) == expected


def test_device_username_exists_str_gives_correct_json_representation():
    _filter = DeviceUsername.exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"EXISTS", "term":"deviceUserName", "value":null}]}'
    assert str(_filter) == expected


def test_device_username_not_exists_str_gives_correct_json_representation():
    _filter = DeviceUsername.not_exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_EXIST", "term":"deviceUserName", "value":null}]}'
    assert str(_filter) == expected


def test_device_username_eq_str_gives_correct_json_representation():
    _filter = DeviceUsername.eq("test_deviceUserName")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"deviceUserName", "value":"test_deviceUserName"}]}'
    assert str(_filter) == expected


def test_device_username_not_eq_str_gives_correct_json_representation():
    _filter = DeviceUsername.not_eq("test_deviceUsername")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"deviceUserName", "value":"test_deviceUsername"}]}'
    assert str(_filter) == expected


def test_device_username_is_in_str_gives_correct_json_representation():
    items = ["deviceUserName1", "deviceUserName2", "deviceUserName3"]
    _filter = DeviceUsername.is_in(items)
    expected = '{"filterClause":"OR", "filters":[{"operator":"IS", "term":"deviceUserName", "value":"deviceUserName1"},{"operator":"IS", "term":"deviceUserName", "value":"deviceUserName2"},{"operator":"IS", "term":"deviceUserName", "value":"deviceUserName3"}]}'
    assert str(_filter) == expected


def test_device_username_not_in_str_gives_correct_json_representation():
    items = ["deviceUserName1", "deviceUserName2", "deviceUserName3"]
    _filter = DeviceUsername.not_in(items)
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"deviceUserName", "value":"deviceUserName1"},{"operator":"IS_NOT", "term":"deviceUserName", "value":"deviceUserName2"},{"operator":"IS_NOT", "term":"deviceUserName", "value":"deviceUserName3"}]}'
    assert str(_filter) == expected


def test_unicode_device_username_eq_str_gives_correct_json_representation():
    unicode_username = u"您已经发现了秘密信息"
    _filter = DeviceUsername.eq(unicode_username)
    expected = u'{"filterClause":"AND", "filters":[{"operator":"IS", "term":"deviceUserName", "value":"\u60a8\u5df2\u7ecf\u53d1\u73b0\u4e86\u79d8\u5bc6\u4fe1\u606f"}]}'
    assert str(_filter) == expected


def test_file_name_exists_str_gives_correct_json_representation():
    _filter = FileName.exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"EXISTS", "term":"fileName", "value":null}]}'
    assert str(_filter) == expected


def test_file_name_not_exists_str_gives_correct_json_representation():
    _filter = FileName.not_exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_EXIST", "term":"fileName", "value":null}]}'
    assert str(_filter) == expected


def test_file_name_eq_str_gives_correct_json_representation():
    _filter = FileName.eq("test_fileName")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"fileName", "value":"test_fileName"}]}'
    assert str(_filter) == expected


def test_file_name_not_eq_str_gives_correct_json_representation():
    _filter = FileName.not_eq("test_fileName")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"fileName", "value":"test_fileName"}]}'
    assert str(_filter) == expected


def test_file_name_is_in_str_gives_correct_json_representation():
    items = ["fileName", "fileName", "fileName"]
    _filter = FileName.is_in(items)
    expected = '{"filterClause":"OR", "filters":[{"operator":"IS", "term":"fileName", "value":"fileName"},{"operator":"IS", "term":"fileName", "value":"fileName"},{"operator":"IS", "term":"fileName", "value":"fileName"}]}'
    assert str(_filter) == expected


def test_file_name_not_in_str_gives_correct_json_representation():
    items = ["fileName1", "fileName2", "fileName3"]
    _filter = FileName.not_in(items)
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"fileName", "value":"fileName1"},{"operator":"IS_NOT", "term":"fileName", "value":"fileName2"},{"operator":"IS_NOT", "term":"fileName", "value":"fileName3"}]}'
    assert str(_filter) == expected


def test_file_path_exists_str_gives_correct_json_representation():
    _filter = FilePath.exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"EXISTS", "term":"filePath", "value":null}]}'
    assert str(_filter) == expected


def test_file_path_not_exists_str_gives_correct_json_representation():
    _filter = FilePath.not_exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_EXIST", "term":"filePath", "value":null}]}'
    assert str(_filter) == expected


def test_file_path_eq_str_gives_correct_json_representation():
    _filter = FilePath.eq("test_filePath")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"filePath", "value":"test_filePath"}]}'
    assert str(_filter) == expected


def test_file_path_not_eq_str_gives_correct_json_representation():
    _filter = FilePath.not_eq("test_filePath")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"filePath", "value":"test_filePath"}]}'
    assert str(_filter) == expected


def test_file_path_is_in_str_gives_correct_json_representation():
    items = ["filePath1", "filePath2", "filePath3"]
    _filter = FilePath.is_in(items)
    expected = '{"filterClause":"OR", "filters":[{"operator":"IS", "term":"filePath", "value":"filePath1"},{"operator":"IS", "term":"filePath", "value":"filePath2"},{"operator":"IS", "term":"filePath", "value":"filePath3"}]}'
    assert str(_filter) == expected


def test_file_path_not_in_str_gives_correct_json_representation():
    items = ["filePath1", "filePath2", "filePath3"]
    _filter = FilePath.not_in(items)
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"filePath", "value":"filePath1"},{"operator":"IS_NOT", "term":"filePath", "value":"filePath2"},{"operator":"IS_NOT", "term":"filePath", "value":"filePath3"}]}'
    assert str(_filter) == expected


def test_public_ip_exists_str_gives_correct_json_representation():
    _filter = PublicIPAddress.exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"EXISTS", "term":"publicIpAddress", "value":null}]}'
    assert str(_filter) == expected


def test_public_ip_not_exists_str_gives_correct_json_representation():
    _filter = PublicIPAddress.not_exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_EXIST", "term":"publicIpAddress", "value":null}]}'
    assert str(_filter) == expected


def test_public_ip_address_eq_str_gives_correct_json_representation():
    _filter = PublicIPAddress.eq("test_publicIp")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"publicIpAddress", "value":"test_publicIp"}]}'
    assert str(_filter) == expected


def test_public_ip_address_not_eq_str_gives_correct_json_representation():
    _filter = PublicIPAddress.not_eq("test_publicIp")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"publicIpAddress", "value":"test_publicIp"}]}'
    assert str(_filter) == expected


def test_public_ip_address_is_in_str_gives_correct_json_representation():
    items = ["publicIpAddress1", "publicIpAddress2", "publicIpAddress3"]
    _filter = PublicIPAddress.is_in(items)
    expected = '{"filterClause":"OR", "filters":[{"operator":"IS", "term":"publicIpAddress", "value":"publicIpAddress1"},{"operator":"IS", "term":"publicIpAddress", "value":"publicIpAddress2"},{"operator":"IS", "term":"publicIpAddress", "value":"publicIpAddress3"}]}'
    assert str(_filter) == expected


def test_public_ip_address_not_in_str_gives_correct_json_representation():
    items = ["publicIpAddress1", "publicIpAddress2", "publicIpAddress3"]
    _filter = PublicIPAddress.not_in(items)
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"publicIpAddress", "value":"publicIpAddress1"},{"operator":"IS_NOT", "term":"publicIpAddress", "value":"publicIpAddress2"},{"operator":"IS_NOT", "term":"publicIpAddress", "value":"publicIpAddress3"}]}'
    assert str(_filter) == expected


def test_private_ip_exists_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"EXISTS", "term":"privateIpAddresses", "value":null}]}'
    assert str(_filter) == expected


def test_private_ip_not_exists_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.not_exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_EXIST", "term":"privateIpAddresses", "value":null}]}'
    assert str(_filter) == expected


def test_private_ip_address_eq_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.eq("test_privateIp")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"privateIpAddresses", "value":"test_privateIp"}]}'
    assert str(_filter) == expected


def test_private_ip_address_not_eq_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.not_eq("test_privateIp")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"privateIpAddresses", "value":"test_privateIp"}]}'
    assert str(_filter) == expected


def test_private_ip_address_is_in_str_gives_correct_json_representation():
    items = ["privateIp1", "privateIp2", "privateIp3"]
    _filter = PrivateIPAddress.is_in(items)
    expected = '{"filterClause":"OR", "filters":[{"operator":"IS", "term":"privateIpAddresses", "value":"privateIp1"},{"operator":"IS", "term":"privateIpAddresses", "value":"privateIp2"},{"operator":"IS", "term":"privateIpAddresses", "value":"privateIp3"}]}'
    assert str(_filter) == expected


def test_private_ip_address_not_in_str_gives_correct_json_representation():
    items = ["privateIp1", "privateIp2", "privateIp3"]
    _filter = PrivateIPAddress.not_in(items)
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"privateIpAddresses", "value":"privateIp1"},{"operator":"IS_NOT", "term":"privateIpAddresses", "value":"privateIp2"},{"operator":"IS_NOT", "term":"privateIpAddresses", "value":"privateIp3"}]}'
    assert str(_filter) == expected


def test_event_type_exists_str_gives_correct_json_representation():
    _filter = EventType.exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"EXISTS", "term":"eventType", "value":null}]}'
    assert str(_filter) == expected


def test_event_type_not_exists_str_gives_correct_json_representation():
    _filter = EventType.not_exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_EXIST", "term":"eventType", "value":null}]}'
    assert str(_filter) == expected


def test_event_type_eq_str_gives_correct_json_representation():
    _filter = EventType.eq("test_eventType")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"eventType", "value":"test_eventType"}]}'
    assert str(_filter) == expected


def test_event_type_not_eq_str_gives_correct_json_representation():
    _filter = EventType.not_eq("test_eventType")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"eventType", "value":"test_eventType"}]}'
    assert str(_filter) == expected


def test_event_type_is_in_str_gives_correct_json_representation():
    items = ["eventType1", "eventType2", "eventType3"]
    _filter = EventType.is_in(items)
    expected = '{"filterClause":"OR", "filters":[{"operator":"IS", "term":"eventType", "value":"eventType1"},{"operator":"IS", "term":"eventType", "value":"eventType2"},{"operator":"IS", "term":"eventType", "value":"eventType3"}]}'
    assert str(_filter) == expected


def test_event_type_not_in_str_gives_correct_json_representation():
    items = ["eventType1", "eventType2", "eventType3"]
    _filter = EventType.not_in(items)
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"eventType", "value":"eventType1"},{"operator":"IS_NOT", "term":"eventType", "value":"eventType2"},{"operator":"IS_NOT", "term":"eventType", "value":"eventType3"}]}'
    assert str(_filter) == expected


def test_exposure_type_exists_str_gives_correct_json_representation():
    _filter = ExposureType.exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"EXISTS", "term":"exposure", "value":null}]}'
    assert str(_filter) == expected


def test_exposure_type_not_exists_str_gives_correct_json_representation():
    _filter = ExposureType.not_exists()
    expected = '{"filterClause":"AND", "filters":[{"operator":"DOES_NOT_EXIST", "term":"exposure", "value":null}]}'
    assert str(_filter) == expected


def test_exposure_type_eq_str_gives_correct_json_representation():
    _filter = ExposureType.eq("test_exposure")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS", "term":"exposure", "value":"test_exposure"}]}'
    assert str(_filter) == expected


def test_exposure_type_not_eq_str_gives_correct_json_representation():
    _filter = ExposureType.not_eq("test_exposure")
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"exposure", "value":"test_exposure"}]}'
    assert str(_filter) == expected


def test_exposure_type_is_in_str_gives_correct_json_representation():
    items = ["exposure1", "exposure2", "exposure3"]
    _filter = ExposureType.is_in(items)
    expected = '{"filterClause":"OR", "filters":[{"operator":"IS", "term":"exposure", "value":"exposure1"},{"operator":"IS", "term":"exposure", "value":"exposure2"},{"operator":"IS", "term":"exposure", "value":"exposure3"}]}'
    assert str(_filter) == expected


def test_exposure_type_not_in_str_gives_correct_json_representation():
    items = ["exposure1", "exposure2", "exposure3"]
    _filter = ExposureType.not_in(items)
    expected = '{"filterClause":"AND", "filters":[{"operator":"IS_NOT", "term":"exposure", "value":"exposure1"},{"operator":"IS_NOT", "term":"exposure", "value":"exposure2"},{"operator":"IS_NOT", "term":"exposure", "value":"exposure3"}]}'
    assert str(_filter) == expected


def test_event_timestamp_on_or_after_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = EventTimestamp.on_or_after(test_time)
    expected = '{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_AFTER", "term":"eventTimestamp", "value":"{0}"}}]}}'.format(
        formatted
    )
    assert str(_filter) == expected


def test_event_timestamp_on_or_before_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = EventTimestamp.on_or_before(test_time)
    expected = '{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_BEFORE", "term":"eventTimestamp", "value":"{}"}}]}}'.format(
        formatted
    )
    assert str(_filter) == expected


def test_event_timestamp_in_range_str_gives_correct_json_representation():
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = format_timestamp(test_before_time)
    formatted_after = format_timestamp(test_after_time)
    _filter = EventTimestamp.in_range(test_before_time, test_after_time)
    expected = '{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_AFTER", "term":"eventTimestamp", "value":"{0}"}},{{"operator":"ON_OR_BEFORE", "term":"eventTimestamp", "value":"{1}"}}]}}'.format(
        formatted_before, formatted_after
    )
    assert str(_filter) == expected


def test_event_timestamp_on_same_day_str_gives_correct_json_representation():
    test_time = time()
    test_date = datetime.utcfromtimestamp(test_time)
    start_time = datetime(test_date.year, test_date.month, test_date.day, 0, 0, 0)
    end_time = datetime(test_date.year, test_date.month, test_date.day, 23, 59, 59)
    formatted_before = format_datetime(start_time)
    formatted_after = format_datetime(end_time)

    _filter = EventTimestamp.on_same_day(test_time)
    expected = '{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_AFTER", "term":"eventTimestamp", "value":"{0}"}},{{"operator":"ON_OR_BEFORE", "term":"eventTimestamp", "value":"{1}"}}]}}'.format(
        formatted_before, formatted_after
    )
    assert str(_filter) == expected


def test_insertion_timestamp_on_or_after_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = InsertionTimestamp.on_or_after(test_time)
    expected = '{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_AFTER", "term":"insertionTimestamp", "value":"{0}"}}]}}'.format(
        formatted
    )
    assert str(_filter) == expected


def test_insertion_timestamp_on_or_before_str_gives_correct_json_representation():
    test_time = time()
    formatted = format_timestamp(test_time)
    _filter = InsertionTimestamp.on_or_before(test_time)
    expected = '{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_BEFORE", "term":"insertionTimestamp", "value":"{0}"}}]}}'.format(
        formatted
    )
    assert str(_filter) == expected


def test_insertion_timestamp_in_range_str_gives_correct_json_representation():
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = format_timestamp(test_before_time)
    formatted_after = format_timestamp(test_after_time)
    _filter = InsertionTimestamp.in_range(test_before_time, test_after_time)
    expected = '{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_AFTER", "term":"insertionTimestamp", "value":"{0}"}},{{"operator":"ON_OR_BEFORE", "term":"insertionTimestamp", "value":"{1}"}}]}}'.format(
        formatted_before, formatted_after
    )
    assert str(_filter) == expected



def test_insertion_timestamp_on_same_day_str_gives_correct_json_representation():
    test_time = time()
    test_date = datetime.utcfromtimestamp(test_time)
    start_time = datetime(test_date.year, test_date.month, test_date.day, 0, 0, 0)
    end_time = datetime(test_date.year, test_date.month, test_date.day, 23, 59, 59)
    formatted_before = format_datetime(start_time)
    formatted_after = format_datetime(end_time)

    _filter = InsertionTimestamp.on_same_day(test_time)
    expected = '{{"filterClause":"AND", "filters":[{{"operator":"ON_OR_AFTER", "term":"insertionTimestamp", "value":"{0}"}},{{"operator":"ON_OR_BEFORE", "term":"insertionTimestamp", "value":"{1}"}}]}}'.format(
        formatted_before, formatted_after
    )
    assert str(_filter) == expected
