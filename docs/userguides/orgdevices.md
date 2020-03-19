# Get Active Devices from an Organization

This is a tutorial on how to get all active devices from an organization using py42.

To begin, we need to initialize the SDK:
```python
import py42.sdk
sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")
```

Get your current organization's org UID using the `py42.sdk.clients.orgs.OrgClient` off the root SDK object. Using the
response, we can get access to the org UID, which will be needed to query devices:
```python
my_org = sdk.orgs.get_current()
org_uid = my_org["orgUid"]
```

Next, we will want to make use of `py42.sdk.clients.devices.DeviceClient` to search for active devices in our
organization. We can achieve this using parameters for the `get_all()` method which pages over Code42 devices:
```python
# Loop over active devices in our organization and print their name and GUID

response = sdk.devices.get_all(active=True, org_uid=org_uid)
for page in response:
    devices = page["computers"]
    for device in devices:
        print(device["osHostname"])
        print(device["guid"])
```

Notice how `get_all()` returns a `generator` object which iterates over pages of devices.

After initializing the SDK, we were able to easily get the devices in our organization.
