# Get Active Devices from an Organization

Sometimes you might want to do something useful that requires information about active devices in your organization.
For example, you might want to create a simple report that illustrates how many devices are running each operating
system in your Code42 environment. The following guide shows the different possible workings for the tools involved in
getting all the active devices in your organization.

To begin, we need to initialize the SDK:
```python
import py42.sdk
sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")
```

### The `DeviceClient.get_all()` Function

Next, we will want to make use of `py42.sdk.clients.devices.DeviceClient` to search for active devices in your
organization. We can achieve this using the `active` parameter on the `get_all()` method.

The `active` parameter has three different states:
* If `active` is set to True, you will only get active devices.
* If `active` is set to False, you will only get deactivated devices.
* If you don't use
`active`, you will get all devices.

The `get_all()` function returns a generator of pages of devices. Depending on your account's role in the
organization, you will get a different list of devices:
* If you are logged in as an ordinary end user, `get_all()` returns all *your* devices.
* If you are logged in as an organization administrator, `get_all()` returns all the devices in your organization.
* If you are a cross-organization administrator, `get_all()` will return all devices across all your organizations.
* Finally, if you are a customer cloud administrator, `get_all()` returns all devices in all organizations.

### Examples

Here is an example using `get_all()` to get all active devices in your organization(s):
```python
# For each device in your organization, print its GUID and operating system

response = sdk.devices.get_all(active=True)
for page in response:
    devices = page["computers"]
    for device in devices:
        print("{0} - {1}".format(device["guid"], device["osName"]))
```
