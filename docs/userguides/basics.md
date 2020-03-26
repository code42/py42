# py42 Basics

Gain confidence in writing your own scripts by learning the basics of py42. The following examples use
`py42.sdk.clients.departing_employee.DepartingEmployeeClient` to demonstrate how to use py42:
* [Initialization](#initialization)
* [Paging](#paging)
* [Py42Response](#py42response)
* [Dates](#dates)
* [Exceptions](#exceptions)

## Initialization

To do anything with py42, you need to initialize the SDK:
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

These methods each return a [python generator](https://wiki.python.org/moin/Generators). By looping over the pages
returned by the generator, we can access the actual list of items we seek. Use the code snippet below as an example
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
`Py42Response.raw_text`) so that it's easier to get the most useful parts of the response. Also, the object is
subscriptable, meaning you can access it with keys or indices (depending on the JSON type underneath `data` on Code42
API responses):
```python
user = response["users"][0]
item = list_response[0]["itemProperty"]
```

To figure out all the keys on a response, you can observe its `.text` attribute. By printing the response, you
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

## Dates

py42 supports [POSIX timestamps](https://en.wikipedia.org/wiki/Unix_time) (seconds) for date parameters. As an
example, see the `departing_on_or_after_epoch` parameter in the
`py42.sdk.clients.departing_employee.DepartingEmployeeClient.get_all()` method.
```python
import py42.sdk
import py42.sdk.util
from datetime import datetime, timedelta
sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")


# Prints all the departing employee cases on or after two weeks

departing_date = datetime.utcnow() + timedelta(days=14)  # How to get a date in the future
epoch = (departing_date - datetime.utcfromtimestamp(0)).total_seconds()  # How to get an epoch time (float)
response = sdk.detectionlists.departing_employee.get_all(departing_on_or_after_epoch=epoch)
for page in response:
    for case in page["cases"]:
        print(case)
```

## Exceptions

py42 throws some of its own exceptions when failures occur. py42 exceptions are found in the `py42.sdk.exceptions`
module. Here are some of the available exceptions:
* `Py42ForbiddenError`: (403) Meaning you don't have the necessary permissions with your currently signed-in account
to perform the action you were trying to do.
* `Py42UnauthorizedError`: (401) Meaning you probably supplied the wrong username or password.
* `Py42InternalServerError`: (500) Meaning it's likely an unhandled issue on our servers.

Let's say you are making a `create_sdk()` function and want to print a more user-friendly message when the provided
username or password are incorrect. This is how you would do that:
```python
import keyring
import py42.sdk
from py42.sdk.exceptions import Py42UnauthorizedError


def create_sdk(username):
    """Tries to initialize SDK. If unauthorized, prints message and exits."""
    try:
        password = keyring.get_password("my_program", username)
        return py42.sdk.from_local_account("www.authority.example.com", username, password)
    except Py42UnauthorizedError:
        print("Invalid username or password.")
        exit(1)
```

In summary, keep in mind that the examples from this guide are intended to be blanket concepts that apply to other
areas in py42. You will page over users and devices the same way you page over departing-employees and alerts.
