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


def test_md5_exists_sets_filter_properties_correctly(exists_filter_creator):
    MD5.exists()
    exists_filter_creator.assert_called_once_with("md5Checksum")


def test_md5_not_exists_sets_filter_properties_correctly(not_exists_filter_creator):
    MD5.not_exists()
    not_exists_filter_creator.assert_called_once_with("md5Checksum")


def test_md5_eq_sets_filter_properties_correctly(eq_filter_creator):
    MD5.eq("test_md5")
    eq_filter_creator.assert_called_once_with("md5Checksum", "test_md5")


def test_md5_not_eq_sets_filter_properties_correctly(not_eq_filter_creator):
    MD5.not_eq("test_md5")
    not_eq_filter_creator.assert_called_once_with("md5Checksum", "test_md5")


def test_md5_is_in_sets_filter_properties_correctly(is_in_filter_creator):
    items = ["md51", "md52", "md53"]
    MD5.is_in(items)
    is_in_filter_creator.assert_called_once_with("md5Checksum", items)


def test_md5_not_in_sets_filter_properties_correctly(not_in_filter_creator):
    items = ["md51", "md52", "md53"]
    MD5.not_in(items)
    not_in_filter_creator.assert_called_once_with("md5Checksum", items)


def test_sha256_exists_sets_filter_properties_correctly(exists_filter_creator):
    SHA256.exists()
    exists_filter_creator.assert_called_once_with("sha256Checksum")


def test_sha256_not_exists_sets_filter_properties_correctly(not_exists_filter_creator):
    SHA256.not_exists()
    not_exists_filter_creator.assert_called_once_with("sha256Checksum")


def test_sha256_eq_sets_filter_properties_correctly(eq_filter_creator):
    SHA256.eq("test_sha256")
    eq_filter_creator.assert_called_once_with("sha256Checksum", "test_sha256")


def test_sha256_not_eq_sets_filter_properties_correctly(not_eq_filter_creator):
    SHA256.not_eq("test_sha256")
    not_eq_filter_creator.assert_called_once_with("sha256Checksum", "test_sha256")


def test_sha256_is_in_sets_filter_properties_correctly(is_in_filter_creator):
    items = ["sha2561", "sha2562", "sha2563"]
    SHA256.is_in(items)
    is_in_filter_creator.assert_called_once_with("sha256Checksum", items)


def test_sha256_not_in_sets_filter_properties_correctly(not_in_filter_creator):
    items = ["sha2561", "sha2562", "sha2563"]
    SHA256.not_in(items)
    not_in_filter_creator.assert_called_once_with("sha256Checksum", items)


def test_os_hostname_exists_sets_filter_properties_correctly(exists_filter_creator):
    OSHostname.exists()
    exists_filter_creator.assert_called_once_with("osHostName")


def test_os_hostname_not_exists_sets_filter_properties_correctly(not_exists_filter_creator):
    OSHostname.not_exists()
    not_exists_filter_creator.assert_called_once_with("osHostName")


def test_os_hostname_eq_sets_filter_properties_correctly(eq_filter_creator):
    OSHostname.eq("test_osHostName")
    eq_filter_creator.assert_called_once_with("osHostName", "test_osHostName")


def test_os_hostname_not_eq_sets_filter_properties_correctly(not_eq_filter_creator):
    OSHostname.not_eq("test_osHostName")
    not_eq_filter_creator.assert_called_once_with("osHostName", "test_osHostName")


def test_os_hostname_is_in_sets_filter_properties_correctly(is_in_filter_creator):
    items = ["osHostName1", "osHostName2", "osHostName3"]
    OSHostname.is_in(items)
    is_in_filter_creator.assert_called_once_with("osHostName", items)


def test_os_hostname_not_in_sets_filter_properties_correctly(not_in_filter_creator):
    items = ["osHostName1", "osHostName2", "osHostName3"]
    OSHostname.not_in(items)
    not_in_filter_creator.assert_called_once_with("osHostName", items)


def test_device_username_exists_sets_filter_properties_correctly(exists_filter_creator):
    DeviceUsername.exists()
    exists_filter_creator.assert_called_once_with("deviceUserName")


def test_device_username_not_exists_sets_filter_properties_correctly(not_exists_filter_creator):
    DeviceUsername.not_exists()
    not_exists_filter_creator.assert_called_once_with("deviceUserName")


def test_device_username_eq_sets_filter_properties_correctly(eq_filter_creator):
    DeviceUsername.eq("test_deviceUserName")
    eq_filter_creator.assert_called_once_with("deviceUserName", "test_deviceUserName")


def test_device_username_not_eq_sets_filter_properties_correctly(not_eq_filter_creator):
    DeviceUsername.not_eq("test_deviceUsername")
    not_eq_filter_creator.assert_called_once_with("deviceUserName", "test_deviceUsername")


def test_device_username_is_in_sets_filter_properties_correctly(is_in_filter_creator):
    items = ["deviceUserName1", "deviceUserName2", "deviceUserName3"]
    DeviceUsername.is_in(items)
    is_in_filter_creator.assert_called_once_with("deviceUserName", items)


def test_device_username_not_in_sets_filter_properties_correctly(not_in_filter_creator):
    items = ["deviceUserName1", "deviceUserName2", "deviceUserName3"]
    DeviceUsername.not_in(items)
    not_in_filter_creator.assert_called_once_with("deviceUserName", items)


def test_unicode_device_username_eq_sets_filter_properties_correctly(eq_filter_creator):
    unicode_username = u"您已经发现了秘密信息"
    DeviceUsername.eq(unicode_username)
    eq_filter_creator.assert_called_once_with("deviceUserName", unicode_username)


def test_file_name_exists_sets_filter_properties_correctly(exists_filter_creator):
    FileName.exists()
    exists_filter_creator.assert_called_once_with("fileName")


def test_file_name_not_exists_sets_filter_properties_correctly(not_exists_filter_creator):
    FileName.not_exists()
    not_exists_filter_creator.assert_called_once_with("fileName")


def test_file_name_eq_sets_filter_properties_correctly(eq_filter_creator):
    FileName.eq("test_fileName")
    eq_filter_creator.assert_called_once_with("fileName", "test_fileName")


def test_file_name_not_eq_sets_filter_properties_correctly(not_eq_filter_creator):
    FileName.not_eq("test_fileName")
    not_eq_filter_creator.assert_called_once_with("fileName", "test_fileName")


def test_file_name_is_in_sets_filter_properties_correctly(is_in_filter_creator):
    items = ["fileName", "fileName", "fileName"]
    FileName.is_in(items)
    is_in_filter_creator.assert_called_once_with("fileName", items)


def test_file_name_not_in_sets_filter_properties_correctly(not_in_filter_creator):
    items = ["fileName1", "fileName2", "fileName3"]
    FileName.not_in(items)
    not_in_filter_creator.assert_called_once_with("fileName", items)


def test_file_path_exists_sets_filter_properties_correctly(exists_filter_creator):
    FilePath.exists()
    exists_filter_creator.assert_called_once_with("filePath")


def test_file_path_not_exists_sets_filter_properties_correctly(not_exists_filter_creator):
    FilePath.not_exists()
    not_exists_filter_creator.assert_called_once_with("filePath")


def test_file_path_eq_sets_filter_properties_correctly(eq_filter_creator):
    FilePath.eq("test_filePath")
    eq_filter_creator.assert_called_once_with("filePath", "test_filePath")


def test_file_path_not_eq_sets_filter_properties_correctly(not_eq_filter_creator):
    FilePath.not_eq("test_filePath")
    not_eq_filter_creator.assert_called_once_with("filePath", "test_filePath")


def test_file_path_is_in_sets_filter_properties_correctly(is_in_filter_creator):
    items = ["filePath1", "filePath2", "filePath3"]
    FilePath.is_in(items)
    is_in_filter_creator.assert_called_once_with("filePath", items)


def test_file_path_not_in_sets_filter_properties_correctly(not_in_filter_creator):
    items = ["filePath1", "filePath2", "filePath3"]
    FilePath.not_in(items)
    not_in_filter_creator.assert_called_once_with("filePath", items)


def test_public_ip_exists_sets_filter_properties_correctly(exists_filter_creator):
    PublicIPAddress.exists()
    exists_filter_creator.assert_called_once_with("publicIpAddress")


def test_public_ip_not_exists_sets_filter_properties_correctly(not_exists_filter_creator):
    PublicIPAddress.not_exists()
    not_exists_filter_creator.assert_called_once_with("publicIpAddress")


def test_public_ip_address_eq_sets_filter_properties_correctly(eq_filter_creator):
    PublicIPAddress.eq("test_publicIp")
    eq_filter_creator.assert_called_once_with("publicIpAddress", "test_publicIp")


def test_public_ip_address_not_eq_sets_filter_properties_correctly(not_eq_filter_creator):
    PublicIPAddress.not_eq("test_publicIp")
    not_eq_filter_creator.assert_called_once_with("publicIpAddress", "test_publicIp")


def test_public_ip_address_is_in_sets_filter_properties_correctly(is_in_filter_creator):
    items = ["publicIpAddress1", "publicIpAddress2", "publicIpAddress3"]
    PublicIPAddress.is_in(items)
    is_in_filter_creator.assert_called_once_with("publicIpAddress", items)


def test_public_ip_address_not_in_sets_filter_properties_correctly(not_in_filter_creator):
    items = ["publicIpAddress1", "publicIpAddress2", "publicIpAddress3"]
    PublicIPAddress.not_in(items)
    not_in_filter_creator.assert_called_once_with("publicIpAddress", items)


def test_private_ip_exists_sets_filter_properties_correctly(exists_filter_creator):
    PrivateIPAddress.exists()
    exists_filter_creator.assert_called_once_with("privateIpAddresses")


def test_private_ip_not_exists_sets_filter_properties_correctly(not_exists_filter_creator):
    PrivateIPAddress.not_exists()
    not_exists_filter_creator.assert_called_once_with("privateIpAddresses")


def test_private_ip_address_eq_sets_filter_properties_correctly(eq_filter_creator):
    PrivateIPAddress.eq("test_privateIp")
    eq_filter_creator.assert_called_once_with("privateIpAddresses", "test_privateIp")


def test_private_ip_address_not_eq_sets_filter_properties_correctly(not_eq_filter_creator):
    PrivateIPAddress.not_eq("test_privateIp")
    not_eq_filter_creator.assert_called_once_with("privateIpAddresses", "test_privateIp")


def test_private_ip_address_is_in_sets_filter_properties_correctly(is_in_filter_creator):
    items = ["privateIp1", "privateIp2", "privateIp3"]
    PrivateIPAddress.is_in(items)
    is_in_filter_creator.assert_called_once_with("privateIpAddresses", items)


def test_private_ip_address_not_in_sets_filter_properties_correctly(not_in_filter_creator):
    items = ["privateIp1", "privateIp2", "privateIp3"]
    PrivateIPAddress.not_in(items)
    not_in_filter_creator.assert_called_once_with("privateIpAddresses", items)


def test_event_type_exists_sets_filter_properties_correctly(exists_filter_creator):
    EventType.exists()
    exists_filter_creator.assert_called_once_with("eventType")


def test_event_type_not_exists_sets_filter_properties_correctly(not_exists_filter_creator):
    EventType.not_exists()
    not_exists_filter_creator.assert_called_once_with("eventType")


def test_event_type_eq_sets_filter_properties_correctly(eq_filter_creator):
    EventType.eq("test_eventType")
    eq_filter_creator.assert_called_once_with("eventType", "test_eventType")


def test_event_type_not_eq_sets_filter_properties_correctly(not_eq_filter_creator):
    EventType.not_eq("test_eventType")
    not_eq_filter_creator.assert_called_once_with("eventType", "test_eventType")


def test_event_type_is_in_sets_filter_properties_correctly(is_in_filter_creator):
    items = ["eventType1", "eventType2", "eventType3"]
    EventType.is_in(items)
    is_in_filter_creator.assert_called_once_with("eventType", items)


def test_event_type_not_in_sets_filter_properties_correctly(not_in_filter_creator):
    items = ["eventType1", "eventType2", "eventType3"]
    EventType.not_in(items)
    not_in_filter_creator.assert_called_once_with("eventType", items)


def test_exposure_type_exists_sets_filter_properties_correctly(exists_filter_creator):
    ExposureType.exists()
    exists_filter_creator.assert_called_once_with("exposure")


def test_exposure_type_not_exists_sets_filter_properties_correctly(not_exists_filter_creator):
    ExposureType.not_exists()
    not_exists_filter_creator.assert_called_once_with("exposure")


def test_exposure_type_eq_sets_filter_properties_correctly(eq_filter_creator):
    ExposureType.eq("test_exposure")
    eq_filter_creator.assert_called_once_with("exposure", "test_exposure")


def test_exposure_type_not_eq_sets_filter_properties_correctly(not_eq_filter_creator):
    ExposureType.not_eq("test_exposure")
    not_eq_filter_creator.assert_called_once_with("exposure", "test_exposure")


def test_exposure_type_is_in_sets_filter_properties_correctly(is_in_filter_creator):
    items = ["exposure1", "exposure2", "exposure3"]
    ExposureType.is_in(items)
    is_in_filter_creator.assert_called_once_with("exposure", items)


def test_exposure_type_not_in_sets_filter_properties_correctly(not_in_filter_creator):
    items = ["exposure1", "exposure2", "exposure3"]
    ExposureType.not_in(items)
    not_in_filter_creator.assert_called_once_with("exposure", items)


def test_event_timestamp_on_or_after_sets_filter_properties_correctly(on_or_after_filter_creator):
    test_time = time()
    formatted = format_timestamp(test_time)
    EventTimestamp.on_or_after(test_time)
    on_or_after_filter_creator.assert_called_once_with("eventTimestamp", formatted)


def test_event_timestamp_on_or_before_sets_filter_properties_correctly(on_or_before_filter_creator):
    test_time = time()
    formatted = format_timestamp(test_time)
    EventTimestamp.on_or_before(test_time)
    on_or_before_filter_creator.assert_called_once_with("eventTimestamp", formatted)


def test_event_timestamp_in_range_sets_filter_properties_correctly(in_range_filter_creator):
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = format_timestamp(test_before_time)
    formatted_after = format_timestamp(test_after_time)
    EventTimestamp.in_range(test_before_time, test_after_time)
    in_range_filter_creator.assert_called_once_with(
        "eventTimestamp", formatted_before, formatted_after
    )


def test_event_timestamp_on_same_day_sets_filter_properties_correctly(in_range_filter_creator):
    test_time = time()
    test_date = datetime.utcfromtimestamp(test_time)
    start_time = datetime(test_date.year, test_date.month, test_date.day, 0, 0, 0)
    end_time = datetime(test_date.year, test_date.month, test_date.day, 0, 23, 59)
    formatted_before = format_datetime(start_time)
    formatted_after = format_datetime(end_time)

    EventTimestamp.on_same_day(test_time)
    in_range_filter_creator.assert_called_once_with(
        "eventTimestamp", formatted_before, formatted_after
    )


def test_insertion_timestamp_on_or_after_sets_filter_properties_correctly(
    on_or_after_filter_creator,
):
    test_time = time()
    formatted = format_timestamp(test_time)
    InsertionTimestamp.on_or_after(test_time)
    on_or_after_filter_creator.assert_called_once_with("insertionTimestamp", formatted)


def test_insertion_timestamp_on_or_before_sets_filter_properties_correctly(
    on_or_before_filter_creator,
):
    test_time = time()
    formatted = format_timestamp(test_time)
    InsertionTimestamp.on_or_before(test_time)
    on_or_before_filter_creator.assert_called_once_with("insertionTimestamp", formatted)


def test_insertion_timestamp_in_range_sets_filter_properties_correctly(in_range_filter_creator):
    test_before_time = time()
    test_after_time = time() + 30  # make sure timestamps are actually different
    formatted_before = format_timestamp(test_before_time)
    formatted_after = format_timestamp(test_after_time)
    InsertionTimestamp.in_range(test_before_time, test_after_time)
    in_range_filter_creator.assert_called_once_with(
        "insertionTimestamp", formatted_before, formatted_after
    )


def test_insertion_timestamp_on_same_day_sets_filter_properties_correctly(in_range_filter_creator):
    test_time = time()
    test_date = datetime.utcfromtimestamp(test_time)
    start_time = datetime(test_date.year, test_date.month, test_date.day, 0, 0, 0)
    end_time = datetime(test_date.year, test_date.month, test_date.day, 0, 23, 59)
    formatted_before = format_datetime(start_time)
    formatted_after = format_datetime(end_time)

    InsertionTimestamp.on_same_day(test_time)
    in_range_filter_creator.assert_called_once_with(
        "insertionTimestamp", formatted_before, formatted_after
    )
