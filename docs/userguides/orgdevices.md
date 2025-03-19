# Get Active Devices From an Organization

Using pycpg, you can retrieve information about the active devices in your organization for various use cases. For example, you might want to create a simple report that illustrates how many devices are running each operating system in your CrashPlan environment. Your user role determines which devices you have access to.

To begin, initialize the SDK:
```python
import pycpg.sdk
sdk = pycpg.sdk.from_local_account("https://console.us1.crashPlan.com", "my_username", "my_password")
```

### The `DeviceClient.get_all()` Function

Next, use `pycpg.sdk.clients.devices.DeviceClient` to search for active devices in your
organization. Use the `active` parameter on the `get_all()` method.

The `active` parameter has three different states:
* If `active` is set to `True`, you will only get active devices.
* If `active` is set to `False`, you will only get deactivated devices.
* If you don't use `active`, you will get all devices.

The `get_all()` function returns a generator of pages of devices. The devices returned by `get_all()` are based on the role and permissions of the user authenticating the SDK.

### Examples

Here is an example using `get_all()` to get all active devices in your organization(s):

```python
# For each active device in your organization, print its GUID and operating system

response = sdk.devices.get_all(active=True)
for page in response:
    devices = page["computers"]
    for device in devices:
        print(f"{device['guid']} - {device['osName']}")
```

As another example, you might have the Cross Org Administrator role and want to get all the active devices for
just one of your organizations.  First use `orgs.get_all()` to return a list of all current organizations and find the UID of the desired organization. Then use the organization's UID to get information on its devices.

```python
# For each active device in the engineering organization, print its GUID and operating system.

# Assume there is only one org named "Engineering"
for page in sdk.orgs.get_all():
    for org in page["orgs"]:
        if org["orgName"] == "Engineering":
            engineering_org_uid = org["orgUid"]
            break

response = sdk.devices.get_all(active=True, org_uid=engineering_org_uid)
for page in response:
    devices = page["computers"]
    for device in devices:
        print(f"{device['guid']} - {device['osName']}")
```

We got the org UID from the engineering organization and then passed it as a parameter to the method to get all the
devices, thus getting all the active devices in the engineering organization.
