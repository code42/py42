# pycpg Basics

This guide explains the basic concepts of pycpg. Learning these basics can help you gain confidence in writing your own
scripts.
- [pycpg Basics](#pycpg-basics)
  - [Initialization](#initialization)
  - [Paging](#paging)
  - [PycpgResponse](#pycpgresponse)
  - [Dates](#dates)
  - [Exceptions](#exceptions)

The examples from this guide are intended as blanket concepts that apply to other areas in pycpg. For example, paging
over users and devices works the same way as over departing employees and alerts.

## Initialization

To use pycpg, you must initialize the SDK:

```python
import pycpg.sdk

sdk = pycpg.sdk.from_local_account("https://console.us1.crashPlan.com", "my_username", "my_password")
```

If your account uses [two-factor authentication](https://support.crashplan.com/hc/en-us/articles/8720828072717-Two-Factor-Authentication-for-CrashPlan), include the time-based one-time password:

```python
sdk = pycpg.sdk.from_local_account("https://console.u1.crashPlan.com", "my_username", "my_password", totp="123456")
```

Alternatively, define a function that returns the time-based one-time password:

```python
def promptForPassword():
    return input("Please input your authentication code: ")

sdk = pycpg.sdk.from_local_account("https://console.us1.crashPlan.com", "my_username", "my_password", totp=promptForPassword)
```

Alternatively, define a function that returns the auth token based on user's authentication approach

```
import json
import requests
from requests.auth import HTTPBasicAuth
def jwt_provider():
    res = requests.get(
            'https://console.us1.crashPlan.com/api/v3/auth/jwt?useBody=true',
            auth=HTTPBasicAuth('username', 'password')
          )
    res_json = json.loads(res.text)
    return res_json['data']['v3_user_token']

sdk_client = pycpg.sdk.from_jwt_provider("https://console.us1.crashPlan.com", jwt_provider)
```


## Paging

pycpg clients often have a method with the name (or name prefix) `get_all`  which handles iterating over pages of
response items. Here are some examples:
* `pycpg.sdk.devices.get_all()`
* `pycpg.sdk.users.get_all()`
* `pycpg.sdk.legalhold.get_all_matters()`
* `pycpg.sdk.orgs.get_all()`

These methods each return a [python generator](https://wiki.python.org/moin/Generators). Looping over the pages
returned by the generator gives you access to the actual list of items. Use the code snippet below as an example
for working with generators and paging in pycpg:

```python
# Prints the username and user ID for all employees included on a watchlist

pages = sdk.watchlists.get_all_included_users(WATCHLIST_ID)  # pages has 'generator' type
for page in pages:  # page has 'PycpgResponse' type
    users = page["includedUsers"]
    for user in users:
        username = user["username"]
        user_id = user["userId"]
        print(f"{username}: {user_id}")
```

Each page is a typical pycpg response. The next section covers what you can do with `PycpgResponse` objects.

## PycpgResponse

pycpg clients return `PycpgResponse` objects which are intentionally similar to `requests.Response` objects.
The `PycpgResponse` class hides unneeded metadata found on the raw `requests.Response.text` (which is available as
`PycpgResponse.raw_text`), making it easier to get the most useful parts of the response. Also, the object is
subscriptable, meaning you can access it with keys or indices (depending on the JSON type underneath `data` on CrashPlan API responses):

```python
user = response["users"][0]
item = list_response[0]["itemProperty"]
```

To see all the keys on a response, observe its `.text` attribute. By printing the response, you
essentially print its text property:

```python
# Prints details about the response from a getting a detection list user.

response = sdk.detectionlists.get_user("test.user@example.com")
print(response)  # JSON as Dictionary - same as print(response.text)
print(response.raw_text)  # Raw API response
print(response.status_code)  # 200
cloud_usernames = response["cloudUsernames"]
# if the response might not contain the property you're looking for,
# check to see if it exists with data.get
cloud_usernames = response.data.get("cloudUsernames")
if cloud_usernames:
    print(cloud_usernames)
```

```{eval-rst}
.. _anchor_dates:
```

## Dates

Most dates in pycpg support [POSIX timestamps](https://en.wikipedia.org/wiki/Unix_time) for date parameters. As an
example, see :class:`sdk.queries.filevents.filters.event_filter.EventTimestamp` which is used for querying file events
by their event timestamp.

```python
from datetime import datetime, timedelta

import pycpg.sdk
import pycpg.util
from pycpg.sdk.queries.fileevents.file_event_query import FileEventQuery
from pycpg.sdk.queries.fileevents.filters.event_filter import EventTimestamp

sdk = pycpg.sdk.from_local_account("https://console.us1.crashPlan.com", "my_username", "my_password")

# Get the epoch date 14 days in the past
query_date = datetime.utcnow() - timedelta(days=14)
query_epoch = (query_date - datetime.utcfromtimestamp(0)).total_seconds()

query = FileEventQuery(EventTimestamp.on_or_after(query_epoch))

response = sdk.securitydata.search_file_events(query)

# Print all the md5 Checksums from every file event within the past 14 days.
file_events = response["fileEvents"]
for event in file_events:
    print(event["md5Checksum"])
```

## Exceptions

pycpg throws some of its own exceptions when failures occur. pycpg exceptions are found in the `pycpg.sdk.exceptions`
module. Some of the available exceptions are:
* `PycpgForbiddenError`: (403) With your currently signed-in account, you don't have the necessary permissions
to perform the action you were trying to do.
* `PycpgUnauthorizedError`: (401) The username or password is incorrect.
* `PycpgInternalServerError`: (500) Likely an unhandled issue on our servers.

For example, you are making a `create_sdk()` function and want to print a more user-friendly message when the provided
username or password are incorrect:

```python
import keyring
import pycpg.sdk
from pycpg.exceptions import PycpgUnauthorizedError


def create_sdk(username):
    """Tries to initialize SDK. If unauthorized, prints message and exits."""
    try:
        password = keyring.get_password("my_program", username)
        return pycpg.sdk.from_local_account("www.authority.example.com", username, password)
    except PycpgUnauthorizedError:
        print("Invalid username or password.")
        exit(1)
```
