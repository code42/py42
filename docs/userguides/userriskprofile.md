# User Risk Profile

A user risk profile is created for each user.  Use py42 to manage these user risk profiles.

## Update a User Risk Profile

Determine the user ID to manage a user's risk profile.  For example, the following code uses the `get_username()` method to find the ID of a user with the username `test.user@code42.com`.

```python
response = sdk.userriskprofile.get_username()

user_id = response.data["userId"]
```

Use the user ID with the `update()` method to manage a user risk profiles' `startDate`, `endDate`, and `notes` fields.

The `startDate` and `endDate` arguments expect a format of `YYYY-MM-DD` or a `datetime` object.

The following code updates the departure date of the user risk profile to March 1st, 2025:

```python
# update the user risk profile
sdk.userriskprofile.update(user_id, end_date="2025-03-01", notes="Updated the departure date.")

# view updated user details
py42.util.print_response(sdk.userriskprofile.get(user_id))
```

If you want to clear a field, provide an empty string to the corresponding argument.

For example, the following code will clear the `endDate` and `notes` fields:

```python
# clear fields on the user risk profile
sdk.userriskprofile.update(user_id, end_date="", notes="")
```

## Manage Cloud Aliases

Each user risk profile starts with a default alias of their code42 username and can have one additional cloud alias.
Use the `UserRiskProfileClient` to manage these aliases.

Use `add_cloud_aliases()` to assign additional cloud aliases to a user:

```python
user_id = "test-user-123"
cloud_aliases = "test-user@email.com"
sdk.userriskprofile.add_cloud_aliases(user_id, cloud_aliases)

# view updated user cloud aliases
py42.util.print_response(sdk.userriskprofile.get(user_id))
```

Remove cloud aliases in a similar manner using the `delete_cloud_aliases()` method. Provide a list of values to add or remove multiple aliases at once.

```python
sdk.userriskprofile.delete_cloud_aliases(user_id, ["test-user@email.com", "username@email.com"])
```
