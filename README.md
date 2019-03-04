
# py42, the Code42 Python SDK

`py42` is a Python wrapper around the Code42 REST APIs that also provides several other useful utility methods.
It is designed to be used for developing your own tools for working with Code42 data while avoiding the overhead
of session / authentication management. 

## Requirements

- Python 2.7.x
- [requests](http://docs.python-requests.org/en/master/)
- Code42 Server 6.8.x+

## Configuration

`py42/settings.py` defines default global settings. To override them, import the settings and override values as
necessary before creating the client. For example, to disable certificate validation in a dev environment: 

```python
import py42.settings as settings
from py42.sdk import SDK

settings.verify_ssl_certs = False
sdk = SDK.create_using_local_account("https://example.code42.com", "foo", "bar")
```

## Usage

The SDK object opens availability to APIs across the Code42 environment, including storage nodes.

```python
from py42.sdk import SDK

sdk = SDK.create_using_local_account("https://example.code42.com", "password", "pw")

# clients are organized by feature groups and accessible under the sdk object
admin_client = sdk.authority.administration
devices_client = sdk.authority.administration.devices
orgs_client = sdk.authority.administration.orgs
users_client = sdk.authority.administration.users

# get information about the current user.
current_user = users_client.get_current_user() 

# get server diagnostic info.
diagnostics = admin_client.get_diagnostics()

# get a list of all devices available to this user.
devices = devices_client.get_devices()

# get a list of all orgs available to this user.
orgs = orgs_client.get_orgs()

# get access to a storage node's APIs.
storage_api = sdk.storage.fetch_client_using_plan_info(init_plan_uid="12345678", init_destination_guid="23456789")
storage_api.security.get_security_detection_events(plan_uid="12345678", include_files=True)
```
