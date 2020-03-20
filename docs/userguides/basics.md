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
`Py42Response` abstracts away metadata found on the raw `requests.Response.text` (which is available as
`Py42Response.raw_text`) so that you only use get useful text. Also, the object is subscriptable, meaning you can
access it with keys or indices:
```python
user = response["users"][0]]
item = list_response[0]["itemProperty"]
```

To figure out all the key on a response, you can observe its `.text` attribute.

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

Use unix epoch time when specifying dates in py42. An example the `departing_on_or_after_epoch` parameter in
`py42.sdk.clients.departing_employee.DepartingEmployeeClient.get_all()` method from the earlier example.

[TODO: ADD TUTORIAL ON DATE EPOCHS - GTG]
