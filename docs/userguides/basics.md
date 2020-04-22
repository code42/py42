# py42 Basics

This guide explains the basic concepts of py42. Learning these basics can help you gain confidence in writing your own scripts. The following examples use
`py42.sdk.clients.departing_employee.DepartingEmployeeClient` to demonstrate how to use py42:
- [py42 Basics](#py42-basics)
  - [Initialization](#initialization)
  - [Paging](#paging)
  - [Py42Response](#py42response)
  - [Dates](#dates)
  - [Exceptions](#exceptions)

The examples from this guide are intended as blanket concepts that apply to other
areas in py42. For example, paging over users and devices works the same way as over departing employees and alerts.

## Initialization

To use py42, you must initialize the SDK:

```python
import py42.sdk

sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")
```

## Paging

py42 clients often have a method with the name (or name prefix) `get_all`  which handles iterating over pages of
response items. Here are some examples:
* `py42.sdk.devices.get_all()`
* `py42.sdk.users.get_all()`
* `py42.sdk.legalhold.get_all_matters()`
* `py42.sdk.orgs.get_all()`

These methods each return a [python generator](https://wiki.python.org/moin/Generators). Looping over the pages
returned by the generator gives you access to the actual list of items. Use the code snippet below as an example
for working with generators and paging in py42:

```python
# Prints the username and notes for all departing employees

pages = sdk.detectionlists.departing_employee.get_all()  # pages has 'generator' type
for page in pages:  # page has 'Py42Response' type
    employees = page["cases"]
    for employee in employees:
        username = employee["userName"]
        notes = employee["notes"]
        print("{0}: {1}".format(employee, notes))
```

Each page is a typical py42 response. The next section covers what you can do with `Py42Response` objects.

## Py42Response

py42 clients return `Py42Response` objects which are intentionally similar to `requests.Response` objects.
The `Py42Response` class hides unneeded metadata found on the raw `requests.Response.text` (which is available as
`Py42Response.raw_text`), making it easier to get the most useful parts of the response. Also, the object is
subscriptable, meaning you can access it with keys or indices (depending on the JSON type underneath `data` on Code42 API responses):

```python
user = response["users"][0]
item = list_response[0]["itemProperty"]
```

To see all the keys on a response, observe its `.text` attribute. By printing the response, you
essentially print its text property:

```python
# Prints details about the response from getting a departing employee

response = sdk.detectionlists.departing_employee.get_by_username("test.user@example.com")
print(response)  # JSON as Dictionary - same as print(response.text)
print(response.raw_text)  # Raw API response
print(response.status_code)  # 200
cloud_usernames = response["cloudUsernames"]
print(cloud_usernames)
```

```eval_rst
.. _anchor_dates:
```

## Exceptions

py42 throws some of its own exceptions when failures occur. py42 exceptions are found in the `py42.sdk.exceptions`
module. Some of the available exceptions are:
* `Py42ForbiddenError`: (403) With your currently signed-in account, you don't have the necessary permissions
to perform the action you were trying to do.
* `Py42UnauthorizedError`: (401) The username or password is incorrect.
* `Py42InternalServerError`: (500) Likely an unhandled issue on our servers.

For example, you are making a `create_sdk()` function and want to print a more user-friendly message when the provided
username or password are incorrect:

```python
import keyring
import py42.sdk
from py42.exceptions import Py42UnauthorizedError


def create_sdk(username):
    """Tries to initialize SDK. If unauthorized, prints message and exits."""
    try:
        password = keyring.get_password("my_program", username)
        return py42.sdk.from_local_account("www.authority.example.com", username, password)
    except Py42UnauthorizedError:
        print("Invalid username or password.")
        exit(1)
```

