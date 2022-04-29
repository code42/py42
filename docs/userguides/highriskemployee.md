# High Risk Employees

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

```{eval-rst}
.. important::
    If the user is already in the High Risk Employee list, you will get a `py42.exceptions.Py42UserAlreadyAddedError`.

```

To remove a user from the High Risk Employee list:
```python
sdk.detectionlists.high_risk_employee.remove(user_id)
```

## Add or Remove Risk Factors From Users

You can add/remove risk factor tags from a high risk user programmatically using the `add_user_risk_tags()` and
`remove_user_risk_tags()` methods in the `detectionlists` module. Both methods take the `user_id` of a high risk employee, and a list of tags that
you want to add/remove:

```python
from py42.constants import RiskTags

tag_list = [RiskTags.CONTRACT_EMPLOYEE, RiskTags.ELEVATED_ACCESS_PRIVILEGES]

# Add the risk tags
response = sdk.detectionlists.add_user_risk_tags(user_id, tag_list)

# Remove the risk tags
response = sdk.detectionlists.remove_user_risk_tags(user_id, tag_list)
```

Constants for Risk tags are available at [Risk Tags](https://py42docs.code42.com/en/stable/methoddocs/constants.html#py42.constants.RiskTags)

For complete details, see
 [High Risk Employee](../methoddocs/detectionlists.md#high-risk-employee).
