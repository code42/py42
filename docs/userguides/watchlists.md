# Watchlists

Use py42 to create and manage watchlists.

Watchlists have replaced the Departing Employees and High Risk Employees detections lists. See the [Code42 Support Documentation](https://support.code42.com/Incydr/Admin/Monitoring_and_managing/Manage_watchlists) on managing watchlists for more information.

## Create a Watchlist

```python
from py42.constants import WatchlistType

watchlist = sdk.watchlists.create(WatchlistType.DEPARTING_EMPLOYEE)

# store the id of the new watchlist
watchlist_id = watchlist.data["watchlistId"]
```

Available watchlist types are available as constants in the [WatchlistType](https://py42docs.code42.com/en/stable/methoddocs/constants.html#py42.constants.WatchlistType) class.

## View Watchlist Details

There are several methods to view different details about watchlists.

```python
import py42.util

# Get information on all current watchlists
response = sdk.watchlists.get_all()

# print all information to the console
for page in response:
    py42.util.print_response(page)
```

Once you have the watchlist's ID, use the following methods to see more details:

```python
# To get watchlist details
sdk.watchlists.get(watchlist_id)

# To see all included users
sdk.watchlists.get_all_included_users(watchlist_id)
```

## Manage Users on Watchlists

Use the `included_users` methods to manage individual users who are explicitly included on watchlists.

Py42 allows you to reference a watchlist either by its ID or by its type. If adding individual users to a watchlist with the `add_included_users_by_watchlist_type()` method, py42 will create the watchlist for you if it doesn't already exist.

For example, Tte following code demonstrates two methods to add users to the Departing Employees watchlist:

```python
user_ids = ["test-user-1@gmail.com", "test-user-2@gmail.com"]

# METHOD 1: add by watchlist id
sdk.watchlists.add_included_users_by_watchlist_id(user_ids, watchlist_id)

# METHOD 2: add by watchlist type
from py42.constants import WatchlistType

# this method will create the DEPARTING_EMPLOYEE watchlist for you if it doesn't already exist
sdk.watchlists.add_included_users_by_watchlist_type(user_ids, WatchlistType.DEPARTING_EMPLOYEE)

# View your updated watchlist users
sdk.watchlists.get_all_included_users(watchlist_id)
```

The `delete_included_users_by_watchlist_id()` and `delete_included_users_by_watchlist_type()` methods can be used similarly to remove users from a watchlist.



