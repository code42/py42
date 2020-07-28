# Add or Remove Users From the Departing Employees List

Use py42 to quickly and easily manage users on the Departing Employees list. This guide describes how to add users to and remove users from the Departing Employees list.

To add a user to the Departing Employees list, all you need to know is the user's Code42 user UID.

To get the user UID based on username:

```python
user = sdk.users.get_by_username("username")
uid = user["users"][0]["userUid"]
```

`user_id` below refers to the user UID.

```python
# Add the departing employee
response = sdk.detectionlists.departing_employee.add(user_id, departure_date)
```

```eval_rst
.. important::
    If the user is already in the Departing Employees list, you will get a response indicating that it is a
    bad request.

    If a detection list user profile doesn't exist yet for this user, one will automatically be created before adding the user to the Departing Employees list.
```

To remove a user from the Departing Employees list:
```python
sdk.detectionlists.departing_employee.remove(user_id)
```

For complete details, see
 [Departing Employee](../methoddocs/detectionlists.html#departing-employee).
