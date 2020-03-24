# Search and Add user to Departing Employee List

Let's say you want to add a user to the departing employee list and all you know is their user UID. We can achieve
this using the `py42.sdk.users.get_by_uid()` method to recover their username, and then use the
`py42.sdk.detectionlists.departing_employee.create()` method which requires a username as a parameter.

This is how you can get the username from the user UID:
```python
user = sdk.users.get_by_uid("895005723650937319")
username = user["username"]
```

Next, use the `py42.sdk.detectionlists.departing_employee.create()` method to add that user to the departing employee
list. Take note of its case ID if you want to do anything else right away:
```python
response = sdk.detectionlists.departing_employee.create(username)  # Add the departing employee
case_id = response["caseId"]  # Make note of its case ID
```

```eval_rst
.. important::
    If the user is already in the departing employee list, you will get a response indicating that it is a
    bad request.
```

The case ID you get back when you create a departing employee is useful for doing other things, such as resolving the
departing employee:
```python
sdk.detectionlists.departing_employee.resolve(case_id)
```

Let's say you do not have the case ID, now what do you do? We can get a case by username using the
`py42.sdk.detectionlists.departing_employee.get_by_username()` method and extract the case ID from the response:
```python
# Resolves departing employee 'test.user@example.com'

employee_item = sdk.detectionlists.departing_employee.get_by_username("test.user@example.com")
case_id = employee_item["caseId"]
sdk.detectionlists.departing_employee.resolve(case_id)
```

In conclusion, you need a username for creating a departing employee and its case ID for doing anything else with that
departing employee. However, there is a way to get departing employee details from just the username, which
contains the case ID you need.
