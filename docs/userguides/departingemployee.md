# Add or Remove user to Departing Employee List

Let's say you want to add a user to the departing employee list then all you need to know is their user UID.

`user_id` below refers to user UID.

```python
# Add the departing employee
response = sdk.detectionlists.departing_employee.add(user_id, departure_date)
```

```eval_rst
.. important::
    If the user is already in the departing employee list, you will get a response indicating that it is a
    bad request.

    A user will be added to detection list profile before adding to departing employee list, if
    profile doesn't exist.
```

To remove a user from departing employee list
```python
sdk.detectionlists.departing_employee.remove(user_id)
```

To get complete options on departing employee
refer [Departing Employee](../methoddocs/detectionlists.html#departing-employee) .

