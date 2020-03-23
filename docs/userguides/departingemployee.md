# Search and Add user to Departing Employee List

Lets say you want to add a user to the departing employee list and all you know is their user UID. We can achieve
this using the `py42.sdk.users.get_by_uid()` method to recover the username, and then use the
`py42.sdk.detectionlists.departing_employee.create()` method which requires a username as its parameter.

This is how you can get the username from the user UID:
```python
user = sdk.users.get_by_uid("895005723650937319")
username = user["username"]
```

Next, the `py42.sdk.detectionlists.departing_employee.create()` method takes a username for adding that user to the
departing employee list:
```python
response = sdk.detectionlists.departing_employee.create(username)  # Add the departing employee
case_id = response["caseId"]  # Make note of its case ID
```

Note that if the user is already added to the departing employee list, you will get a response indicating that it is
a bad request.

The case ID you get back when you create a departing employee is useful for doing other things, such as resolving the
departing employee:
```python
sdk.detectionlists.departing_employee.resolve(case_id)  # This response contains no useful text
```

Let's say you forgot the case ID, now what do you do? We can look at all departing employees and find the one that
matches a given username:
```python
def get_case_id_from_username(username):
    """Searches departing employees for item with given username and returns its case ID."""
    response = sdk.detectionlists.departing_employee.get_all()
    for page in response:
        for case in page["cases"]:
            if case["userName"] == username:
                return case["caseId"]

# Resolve departing employee 'test.user@example.com'

user_to_resolve = "test.user@example.com"
case_id = get_case_id_from_username(user_to_resolve)
sdk.detectionlists.departing_employee.resolve(case_id)
```

In conclusion, you need a username for creating a departing employee and its case ID for doing anything else with that
departing employee.
