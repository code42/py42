# Add or Remove users from the Departing Employee List

Let's say you want to add a user to the departing employee list. All you need to know is the user's Code42 user UID.

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
    If the user is already in the departing employee list, you will get a response indicating that it is a
    bad request.

    if a detection list profile for this user doesn't exist yet, it will automatically be created before adding to the departing employee list. 
```

To remove a user from departing employee list
```python
sdk.detectionlists.departing_employee.remove(user_id)
```

To get complete options on departing employee
refer [Departing Employee](../methoddocs/detectionlists.html#departing-employee) .

