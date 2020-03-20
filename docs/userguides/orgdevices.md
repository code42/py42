# Get Active Devices from an Organization

Sometimes you might want to do something useful that requires information about active devices in your organization.
For example, you might want to create a simple report that illustrates how many devices are running eachoperating system you have in your Code42 environment.


To begin, we need to initialize the SDK:
```python
import py42.sdk
sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")
```

Next, we will want to make use of `py42.sdk.clients.devices.DeviceClient` to search for active devices in our
organization. We can achieve this using the `active` parameter for the `get_all()` method which pages over Code42
devices. If you are logged in as an ordinary end user, `get_all()` returns all your devices. If you are logged in as an
organization administrator, `get_all()` returns all the devices in your organization. If you are a cross-organization
administrator, `get_all()` will return all devices across all your organizations. Finally, if you are a customer cloud
administrator, `get_all()` returns all devices in all organizations.
```python
# For each device in your organization, print its GUID and operating system

response = sdk.devices.get_all(active=True)
for page in response:
    devices = page["computers"]
    for device in devices:
        print("{0} - {1}".format(device["guid"], device["osName"]))
```

Notice how `get_all()` returns a `generator` object which iterates over pages of devices.

After initializing the SDK, we were able to easily get the devices in our organization.
