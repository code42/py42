# py42 Basics

## Initialization

To do anything with py42, you need to initialize the SDK object:
```python
import py42.sdk

sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")
```

## Paging

py42 clients often have a `get_all()` method (or something similar) which handles iterating over pages of response
items. Here are some examples:
* `py42.sdk.devices.get_all()`
* `py42.sdk.users.get_all()`
* `py42.sdk.legalhold.get_all_matters()`
* `py42.sdk.orgs.get_all()`

By looping over the pages returned by the generator object, we can access the list of items we seek. The following
examples use `py42.sdk.clients.departing_employee.DepartingEmployeeClient` to demonstrate basic py42 behaviors, such as
paging.

Use this code snippet as an example for working with generators and paging in py42:
```python
# Print the username and notes for all departing employees

pages = sdk.detectionlists.departing_employee.get_all()  # pages has 'generator' type
for page in pages:  # page has 'Py42Response' type
    employees = page["cases"]
    for employee in employees:
        username = employee["userName"]
        notes = employee["notes"]
        print("{0}: {1}".format(employee, notes))
```

Each page from generator is a typical py42 response. The next section covers the `Py42Response` object.

## Py42Response

py42 clients return `Py42Response` objects which are intentionally similar to `requests.Response` objects.
`Py42Response` hides unneeded metadata found on the raw `requests.Response.text` (which is available as
`Py42Response.raw_text`) so that you only use get useful text. Also, the object is subscriptable, meaning you can
access it with keys or indices:
```python
user = response["users"][0]]
item = list_response[0]["itemProperty"]
```

To figure out all the keys on a response, you can observe its `.text` attribute. By printing the response, you print
its text property:

Here is an example:
```python
# prints details about the response from getting a departing employee

response = sdk.detectionlists.departing_employee.get_by_username("test.user@example.com")
print(response)  # JSON as Dictionary - same as print(response.text)
print(response.raw_text)  # Raw API response
print(response.status_code)  # 200

# prints the cloud usernames from response
cloud_usernames = response["cloudUsernames"]
print(cloud_usernames)
```

## Dates

Use unix epoch time when specifying dates in py42. As an, see the `departing_on_or_after_epoch` parameter in
`py42.sdk.clients.departing_employee.DepartingEmployeeClient.get_all()` method.

```python
import py42.sdk
import py42.sdk.util
from datetime import datetime, timedelta
sdk = py42.sdk.from_local_account("https://console.us.code42.com", "my_username", "my_password")


# Print all the departing employee cases on or after two weeks

departing_date = datetime.utcnow() + timedelta(days=14)
epoch = py42.sdk.util.convert_datetime_to_epoch(departing_date)
response = sdk.detectionlists.departing_employee.get_all(departing_on_or_after_epoch=epoch)
for page in response:
    for case in page["cases"]:
        print(case)
```

## Exceptions

py42 throws some of its own exceptions when things go wrong. The available exceptions are found in the
`py42.sdk.exceptions` module.

Let's say you are making a script for others to use and you want to print a nicer message when initializing the SDK
fails. This is how you would do that:
```python
import keyring
import py42.sdk
from py42.sdk.exceptions import Py42


def authenticate(username):
    try:
        password = keyring.get_password("my_program", username)
        return py42.sdk.from_local_account("www.authority.example.com", username, password)
    except Py42
```
