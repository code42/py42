# Get Active Devices from an Organization

Sometimes you might want to do something useful that requires information about active devices in your organization.
For example, you might want to create a simple report that illustrates how many devices are running each operating
system in your Code42 environment. Your role in the organization determines which devices you have access to.

To begin, we need to initialize the SDK:
```python
import py42.sdk
sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")
```

### The `DeviceClient.get_all()` Function

Next, we will want to make use of `py42.sdk.clients.devices.DeviceClient` to search for active devices in your
organization. We can achieve this using the `active` parameter on the `get_all()` method.

The `active` parameter has three different states:
* If `active` is set to `True`, you will only get active devices.
* If `active` is set to `False`, you will only get deactivated devices.
* If you don't use `active`, you will get all devices.

The `get_all()` function returns a generator of pages of devices. Depending on your account's role in the
organization, you will get different lists of devices:
* If you are logged in as an ordinary end user, `get_all()` returns all *your* devices.
* If you are logged in as an organization administrator, `get_all()` returns all the devices in your organization.
* If you are a cross-organization administrator, `get_all()` returns all devices across all your organizations.
* Finally, if you are a customer cloud administrator, `get_all()` returns all devices in all organizations.

### Examples

Here is an example using `get_all()` to get all active devices in your organization(s):

```python
# For each active device in your organization, print its GUID and operating system

response = sdk.devices.get_all(active=True)
for page in response:
    devices = page["computers"]
    for device in devices:
        print("{0} - {1}".format(device["guid"], device["osName"]))
```

Another example might be that you are a cross-organization administrator and you wish to get all the active devices for
just one of your organizations. To do this, we can make use of the `py42.sdk.clients.devices.OrgClient.get_by_name()`
method. The `get_by_name()` method returns a list of organizations matching the name you give it.

```python
# For each active device in the engineering organization, print its GUID and operating system.

# Assume there is only one org named "Engineering"
engineering_org = sdk.orgs.get_by_name("Engineering")[0]
engineering_org_uid = engineering_org["orgUid"]
response = sdk.devices.get_all(active=True, org_uid=engineering_org_uid)
for page in response:
    devices = page["computers"]
    for device in devices:
        print("{0} - {1}".format(device["guid"], device["osName"]))
```

We got the org UID from the engineering organization and then passed it as a parameter to the method to get all the
devices, thus getting all the active devices in the engineering organization.
