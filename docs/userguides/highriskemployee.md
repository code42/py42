# High Risk Employee

## Add or Remove Users From the High Risk Employee List

Use py42 to quickly and easily manage users on the High Risk Employee list. This guide describes how to add users to and
remove users from the High Risk Employee list.

To add a user to the High Risk Employees list, all you need to know is the user's Code42 user UID.

To get the user UID based on username:

```python
user = sdk.users.get_by_username("username")
uid = user["users"][0]["userUid"]
```

`user_id` below refers to the user UID.

```python
# Add the high risk employee
response = sdk.detectionlists.high_risk_employee.add(user_id)
```

```eval_rst
.. important::
    If the user is already in the High Risk Employee list, you will get a response indicating that it is a
    bad request.

    If a detection list user profile doesn't exist yet for this user, one will automatically be created before adding
    the user to the High Risk Employee list.
```

To remove a user from the High Risk Employee list:
```python
sdk.detectionlists.high_risk_employee.remove(user_id)
```

For complete details, see
 [High Risk Employee](../methoddocs/detectionlists.html#high-risk-employee).


##
 Add or Remove Risk Factors From Users

You can add/remove risk factor tags from a user programmatically using the `add_user_risk_tags()` and
`remove_user_risk_tags()` methods in the `detectionlists` module. Both methods take a user_id and a list of tags that
you want to add/remove:

```python
tag_list = ["CONTRACT_EMPLOYEE", "ELEVATED_ACCESS_PRIVILEGES"]

# Add the risk tags
response = sdk.detectionlists.add_user_risk_tags(user_id, tag_list)

# Remove the risk tags
response = sdk.detectionlists.remove_user_risk_tags(user_id, tag_list)
```

The available risk tags are:

- `HIGH_IMPACT_EMPLOYEE`
- `ELEVATED_ACCESS_PRIVILEGES`
- `PERFORMANCE_CONCERNS`
- `FLIGHT_RISK`
- `SUSPICIOUS_SYSTEM_ACTIVITY`
- `POOR_SECURITY_PRACTICES`
- `CONTRACT_EMPLOYEE`
