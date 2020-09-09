# -*- coding: utf-8 -*-
import pytest
from tests.sdk.queries.conftest import EXISTS
from tests.sdk.queries.conftest import IS
from tests.sdk.queries.conftest import IS_IN
from tests.sdk.queries.conftest import IS_NOT
from tests.sdk.queries.conftest import NOT_EXISTS
from tests.sdk.queries.conftest import NOT_IN

from py42._internal.compat import str
from py42.sdk.queries.fileevents.filters.device_filter import DeviceSignedInUserName
from py42.sdk.queries.fileevents.filters.device_filter import DeviceUsername
from py42.sdk.queries.fileevents.filters.device_filter import OSHostname
from py42.sdk.queries.fileevents.filters.device_filter import PrivateIPAddress
from py42.sdk.queries.fileevents.filters.device_filter import PublicIPAddress


def test_device_username_exists_str_gives_correct_json_representation():
    _filter = DeviceUsername.exists()
    expected = EXISTS.format("deviceUserName")
    assert str(_filter) == expected


def test_device_username_not_exists_str_gives_correct_json_representation():
    _filter = DeviceUsername.not_exists()
    expected = NOT_EXISTS.format("deviceUserName")
    assert str(_filter) == expected


def test_device_username_eq_str_gives_correct_json_representation():
    _filter = DeviceUsername.eq("test_deviceUserName")
    expected = IS.format("deviceUserName", "test_deviceUserName")
    assert str(_filter) == expected


def test_device_username_not_eq_str_gives_correct_json_representation():
    _filter = DeviceUsername.not_eq("test_deviceUserName")
    expected = IS_NOT.format("deviceUserName", "test_deviceUserName")
    assert str(_filter) == expected


def test_device_username_is_in_str_gives_correct_json_representation():
    items = ["deviceUserName1", "deviceUserName2", "deviceUserName3"]
    _filter = DeviceUsername.is_in(items)
    expected = IS_IN.format("deviceUserName", *items)
    assert str(_filter) == expected


def test_device_username_not_in_str_gives_correct_json_representation():
    items = ["deviceUserName1", "deviceUserName2", "deviceUserName3"]
    _filter = DeviceUsername.not_in(items)
    expected = NOT_IN.format("deviceUserName", *items)
    assert str(_filter) == expected


def test_device_username_eq_unicode_str_gives_correct_json_representation():
    unicode_username = u"您已经发现了秘密信息"
    _filter = DeviceUsername.eq(unicode_username)
    expected = IS.format(
        u"deviceUserName",
        u"\u60a8\u5df2\u7ecf\u53d1\u73b0\u4e86\u79d8\u5bc6\u4fe1\u606f",
    )
    assert str(_filter) == expected


def test_os_hostname_exists_str_gives_correct_json_representation():
    _filter = OSHostname.exists()
    expected = EXISTS.format("osHostName")
    assert str(_filter) == expected


def test_os_hostname_not_exists_str_gives_correct_json_representation():
    _filter = OSHostname.not_exists()
    expected = NOT_EXISTS.format("osHostName")
    assert str(_filter) == expected


def test_os_hostname_eq_str_gives_correct_json_representation():
    _filter = OSHostname.eq("test_osHostName")
    expected = IS.format("osHostName", "test_osHostName")
    assert str(_filter) == expected


def test_os_hostname_not_eq_str_gives_correct_json_representation():
    _filter = OSHostname.not_eq("test_osHostName")
    expected = IS_NOT.format("osHostName", "test_osHostName")
    assert str(_filter) == expected


def test_os_hostname_is_in_str_gives_correct_json_representation():
    items = ["osHostName1", "osHostName2", "osHostName3"]
    _filter = OSHostname.is_in(items)
    expected = IS_IN.format("osHostName", *items)
    assert str(_filter) == expected


def test_os_hostname_not_in_str_gives_correct_json_representation():
    items = ["osHostName1", "osHostName2", "osHostName3"]
    _filter = OSHostname.not_in(items)
    expected = NOT_IN.format("osHostName", *items)
    assert str(_filter) == expected


def test_private_ip_exists_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.exists()
    expected = EXISTS.format("privateIpAddresses")
    assert str(_filter) == expected


def test_private_ip_not_exists_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.not_exists()
    expected = NOT_EXISTS.format("privateIpAddresses")
    assert str(_filter) == expected


def test_private_ip_address_eq_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.eq("test_privateIp")
    expected = IS.format("privateIpAddresses", "test_privateIp")
    assert str(_filter) == expected


def test_private_ip_address_not_eq_str_gives_correct_json_representation():
    _filter = PrivateIPAddress.not_eq("test_privateIp")
    expected = IS_NOT.format("privateIpAddresses", "test_privateIp")
    assert str(_filter) == expected


def test_private_ip_address_is_in_str_gives_correct_json_representation():
    items = ["privateIp1", "privateIp2", "privateIp3"]
    _filter = PrivateIPAddress.is_in(items)
    expected = IS_IN.format("privateIpAddresses", *items)
    assert str(_filter) == expected


def test_private_ip_address_not_in_str_gives_correct_json_representation():
    items = ["privateIp1", "privateIp2", "privateIp3"]
    _filter = PrivateIPAddress.not_in(items)
    expected = NOT_IN.format("privateIpAddresses", *items)
    assert str(_filter) == expected


def test_public_ip_address_exists_str_gives_correct_json_representation():
    _filter = PublicIPAddress.exists()
    expected = EXISTS.format("publicIpAddress")
    assert str(_filter) == expected


def test_public_ip_address_not_exists_str_gives_correct_json_representation():
    _filter = PublicIPAddress.not_exists()
    expected = NOT_EXISTS.format("publicIpAddress")
    assert str(_filter) == expected


def test_public_ip_address_eq_str_gives_correct_json_representation():
    _filter = PublicIPAddress.eq("test_publicIp")
    expected = IS.format("publicIpAddress", "test_publicIp")
    assert str(_filter) == expected


def test_public_ip_address_not_eq_str_gives_correct_json_representation():
    _filter = PublicIPAddress.not_eq("test_publicIp")
    expected = IS_NOT.format("publicIpAddress", "test_publicIp")
    assert str(_filter) == expected


def test_public_ip_address_is_in_str_gives_correct_json_representation():
    items = ["publicIpAddress1", "publicIpAddress2", "publicIpAddress3"]
    _filter = PublicIPAddress.is_in(items)
    expected = IS_IN.format("publicIpAddress", *items)
    assert str(_filter) == expected


def test_public_ip_address_not_in_str_gives_correct_json_representation():
    items = ["publicIpAddress1", "publicIpAddress2", "publicIpAddress3"]
    _filter = PublicIPAddress.not_in(items)
    expected = NOT_IN.format("publicIpAddress", *items)
    assert str(_filter) == expected


@pytest.mark.parametrize(
    "filter_criteria, test_filter",
    [(DeviceSignedInUserName.eq, IS), (DeviceSignedInUserName.not_eq, IS_NOT)],
)
def test_equality_device_signed_in_username_gives_correct_json_representation(
    filter_criteria, test_filter
):
    _filter = filter_criteria("username")
    expected = test_filter.format("operatingSystemUser", "username")
    assert str(_filter) == expected


@pytest.mark.parametrize(
    "filter_criteria, test_filter",
    [(DeviceSignedInUserName.is_in, IS_IN), (DeviceSignedInUserName.not_in, NOT_IN)],
)
def test_multi_vlaue_device_signed_in_username_gives_correct_json_representation(
    filter_criteria, test_filter
):
    usernames = ["username1", "username2", "username3"]
    _filter = filter_criteria(usernames)
    expected = test_filter.format("operatingSystemUser", *usernames)
    assert str(_filter) == expected
