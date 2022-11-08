from py42.exceptions import Py42BadRequestError
from py42.exceptions import Py42Error
from py42.exceptions import Py42InvalidWatchlistType
from py42.exceptions import Py42NotFoundError
from py42.exceptions import Py42WatchlistNotFound
from py42.exceptions import Py42WatchlistOrUserNotFound
from py42.services import BaseService
from py42.services.util import get_all_pages


class WatchlistsService(BaseService):

    _uri_prefix = "/v1/watchlists"

    def __init__(self, connection):
        super().__init__(connection)
        self._watchlist_type_id_map = {}

    @property
    def watchlist_type_id_map(self):
        """Map watchlist types to IDs, if they exist."""
        if not self._watchlist_type_id_map:
            self._watchlist_type_id_map = {}
            watchlists = self.get_page(page_size=100).data["watchlists"]
            for item in watchlists:
                # We will need to custom handle CUSTOM types when they come around
                self._watchlist_type_id_map[item["listType"]] = item["watchlistId"]
        return self._watchlist_type_id_map

    def get(self, watchlist_id):
        uri = f"{self._uri_prefix}/{watchlist_id}"
        try:
            return self._connection.get(uri)
        except Py42NotFoundError as err:
            raise Py42WatchlistNotFound(err, watchlist_id)

    def delete(self, watchlist_id):
        uri = f"{self._uri_prefix}/{watchlist_id}"
        try:
            response = self._connection.delete(uri)
            # delete dictionary entry if success
            if response.status_code == 200:
                for k, v in self.watchlist_type_id_map.items():
                    if v == watchlist_id:
                        del self.watchlist_type_id_map[k]
                        break
            return response
        except Py42NotFoundError as err:
            raise Py42WatchlistNotFound(err, watchlist_id)

    def get_page(self, page_num=1, page_size=None):
        data = {
            "page": page_num,
            "page_size": page_size,
        }
        return self._connection.get(self._uri_prefix, params=data)

    def get_all(self):
        return get_all_pages(self.get_page, "watchlists")

    def create(self, watchlist_type, title=None, description=None):
        data = {
            "watchlistType": watchlist_type,
            "title": title,
            "description": description,
        }
        try:
            response = self._connection.post(self._uri_prefix, json=data)
            self.watchlist_type_id_map[watchlist_type] = response.data["watchlistId"]
            return response
        except Py42BadRequestError as err:
            if (
                f"Error converting value \\\"{watchlist_type}\\\" to type 'WatchlistSdk.Model.WatchlistType'."
                in err.response.text
            ):
                raise Py42InvalidWatchlistType(err, watchlist_type)
            # Api handles Watchlist_Type_Unspecified Case

    def get_page_included_users(self, watchlist_id, page_num=1, page_size=None):
        data = {
            "page": page_num,
            "page_size": page_size,
        }
        uri = f"{self._uri_prefix}/{watchlist_id}/included-users"
        return self._connection.get(uri, params=data)

    def get_all_included_users(self, watchlist_id):
        return get_all_pages(
            self.get_page_included_users, "includedUsers", watchlist_id=watchlist_id
        )

    def add_included_users_by_watchlist_id(self, user_ids, watchlist_id):
        if not isinstance(user_ids, (list, tuple)):
            user_ids = [user_ids]
        data = {"userIds": user_ids, "watchlistId": watchlist_id}
        uri = f"{self._uri_prefix}/{watchlist_id}/included-users/add"
        try:
            return self._connection.post(uri, json=data)
        except Py42BadRequestError as err:
            if "Watchlist not found" in err.response.text:
                raise Py42WatchlistNotFound(err, watchlist_id)
            if "User not found" in err.response.text:
                raise Py42NotFoundError(err, message=err.response.text)
            raise

    def add_included_users_by_watchlist_type(self, user_ids, watchlist_type):
        try:
            id = self.watchlist_type_id_map[watchlist_type]
        except KeyError:
            # if watchlist of specified type not found, create watchlist
            id = (self.create(watchlist_type)).data["watchlistId"]
        return self.add_included_users_by_watchlist_id(user_ids, id)

    def delete_included_users_by_watchlist_id(self, user_ids, watchlist_id):
        if not isinstance(user_ids, (list, tuple)):
            user_ids = [user_ids]
        data = {"userIds": user_ids, "watchlistId": watchlist_id}
        uri = f"{self._uri_prefix}/{watchlist_id}/included-users/delete"
        try:
            return self._connection.post(uri, json=data)
        except Py42BadRequestError as err:
            if "Watchlist not found" in err.response.text:
                raise Py42WatchlistNotFound(err, watchlist_id)
            if "User not found" in err.response.text:
                raise Py42NotFoundError(err, message=err.response.text)
            raise

    def delete_included_users_by_watchlist_type(self, user_ids, watchlist_type):
        try:
            id = self.watchlist_type_id_map[watchlist_type]
        except KeyError:
            # if specified watchlist type not found, raise error
            raise Py42Error(f"Couldn't find watchlist of type:'{watchlist_type}'.")
        return self.delete_included_users_by_watchlist_id(user_ids, id)

    def get_page_watchlist_members(self, watchlist_id, page_num=1, page_size=None):
        data = {
            "page": page_num,
            "page_size": page_size,
        }
        uri = f"{self._uri_prefix}/{watchlist_id}/members"
        try:
            return self._connection.get(uri, params=data)
        except Py42NotFoundError as err:
            raise Py42WatchlistNotFound(err, watchlist_id)

    def get_all_watchlist_members(self, watchlist_id):
        return get_all_pages(
            self.get_page_watchlist_members,
            "watchlistMembers",
            watchlist_id=watchlist_id,
        )

    def get_watchlist_member(self, watchlist_id, user_id):
        uri = f"{self._uri_prefix}/{watchlist_id}/members/{user_id}"
        try:
            return self._connection.get(uri)
        except Py42NotFoundError as err:
            raise Py42WatchlistOrUserNotFound(err, watchlist_id, user_id)
