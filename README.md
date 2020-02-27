
# py42, the official Code42 Python SDK

![Build status](https://github.com/code42/py42/workflows/build/badge.svg)
[![versions](https://img.shields.io/pypi/pyversions/py42.svg)](https://pypi.org/project/py42/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


`py42` is a Python wrapper around the Code42 REST APIs that also provides several other useful utility methods.
It is designed to be used for developing your own tools for working with Code42 data while avoiding the overhead
of session / authentication management. 

## Requirements

- Python 2.7.x or 3.5.0+
- Code42 Server 6.8.x+

## Installation

Run the `setup.py` script to install the py42 package and its dependencies on your system. 
You will likely need administrative privileges for this.

```bash
$ python setup.py install
```

## Hello, py42

Here's a simple example to verify the installation and your server/account.

Launch the Python interpreter

```bash
$ python
```

Import a couple essentials

```python
>>> from py42.sdk import SDK
>>> import py42.util as util
```

Initialize the client.

```python
>>> sdk = SDK.create_using_local_account("https://console.us.code42.com", "john.doe", "password")
```

Get and print your user information.

```python
>>> response = sdk.users.get_current_user()
>>> util.print_response(response)
```

You should see something like the following:

```json
{
    "data": {
        "username": "john.doe",
        "orgName": "ACME Organization",
        "userId": 123456,
        "emailPromo": true,
        "licenses": [],
        "modificationDate": "2018-08-29T15:32:56.995-05:00",
        "blocked": false,
        "usernameIsAnEmail": true,
        "userUid": "1234567890abcdef",
        "userExtRef": null,
        "email": "john.doe@acme.com",
        "status": "Active",
        "localAuthenticationOnly": false,
        "orgUid": "123456789123456789",
        "passwordReset": true,
        "active": true,
        "creationDate": "2012-01-16T11:25:43.545-06:00",
        "orgType": "BUSINESS",
        "firstName": "John",
        "lastName": "Doe",
        "notes": null,
        "orgId": 123456,
        "quotaInBytes": -1,
        "invited": false
    },
    "metadata": {
        "timestamp": "2019-03-05T06:06:31.438-06:00",
        "params": {}
    }
}
```


## Configuration

There are a few default settings that affect the behavior of the client.

| Name | Description | Default |
| ---- | ----------- | ------- |
| verify_ssl_certs | Controls whether the SDK verifies the server's certificate.<br>Possible values: `True`, `False`, or a path to a CA bundle to use.| `True`
| proxies | Dictionary mapping protocol or protocol and hostname to the URL of the proxy.<br>See [the Requests library's documentation on proxies](http://docs.python-requests.org/en/master/user/advanced/?highlight=proxies#proxies) for more info.| `None`
| debug_level | Controls print statements for debugging | `py42.debug_level.NONE`
| items_per_page | Controls how many items are retrieved per request for methods that loops over several "pages" of items in order to collect them all. | 1000

To override these settings, import `py42.settings` and override values as necessary before creating the client.
 For example, to disable certificate validation in a dev environment: 

```python
import py42.settings as settings
from py42.sdk import SDK

settings.verify_ssl_certs = False
sdk = SDK.create_using_local_account("https://console.us.code42.com", "my_username", "my_password")
```

## Usage

The SDK object opens availability to APIs across the Code42 environment, including storage nodes.

```python
from py42.sdk import SDK

sdk = SDK.create_using_local_account("https://console.us.code42.com", "my_username", "my_password")

# clients are organized by feature groups and accessible under the sdk object

# get information about the current user.
current_user = sdk.users.get_current_user() 

# get server diagnostic info.
diagnostics = sdk.administration.get_diagnostics()

# get a list of all devices available to this user.
devices = sdk.devices.get_devices()

# get a list of all orgs available to this user.
orgs = sdk.orgs.get_all()

# save a copy of a file from an archive this user has access to into the current working directory.
sdk.archive.download_from_backup("/full/path/to/file.txt", "1234567890")

# search file events
from py42.sdk.file_event_query import *
query = FileEventQuery.all(MD5.eq("e804d1eb229298b04522c5504b8131f0"))
file_events = sdk.security.search_file_events(query)
```

## Additional Resources

For complete documentation on the Code42 web API that backs this SDK, here are some helpful resources:

- [Introduction to the Code42 API](https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Introduction_to_the_Code42_API)
- [Code42 API documentation viewers](https://support.code42.com/Administrator/Cloud/Monitoring_and_managing/Introduction_to_the_Code42_API/Code42_API_documentation_viewer)
