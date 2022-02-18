# Departing Employees

## Add or Remove Users From the Departing Employees List

Use py42 to quickly and easily manage users on the Departing Employees list. This guide describes how to add users to and remove users from the Departing Employees list.

To add a user to the Departing Employees list, all you need to know is the user's Code42 user UID.

To get the user UID based on username:

```python
user = sdk.users.get_by_username("username")
uid = user["users"][0]["userUid"]
```

`user_id` below refers to the user UID.

```python
from py42.exceptions import Py42UserAlreadyAddedError

# Add the departing employee
try:
    response = sdk.detectionlists.departing_employee.add(user_id, departure_date)
except Py42UserAlreadyAddedError:
    print("The user is already on the Departing Employee list.")
```

```{eval-rst}
.. important::
    If the user is already in the Departing Employees list, you will get an `py42.exceptions.Py42UserAlreadyAddedError`.

```

To remove a user from the Departing Employees list:
```python
sdk.detectionlists.departing_employee.remove(user_id)
```

For complete details, see
 [Departing Employee](../methoddocs/detectionlists.html#departing-employee).
