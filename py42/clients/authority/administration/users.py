from py42 import util
from py42.clients.authority.authority_base import AuthorityTargetedClient
import json


class UserClient(AuthorityTargetedClient):

    def create_user(self, org_uid, username, email=None, password=None, first_name=None, last_name=None, notes=None,
                    **kwargs):
        uri = "/api/User/"
        data = {"orgUid": org_uid, "username": username, "email": email, "password": password, "firstName": first_name,
                "lastName": last_name, "notes": notes}
        return self.post(uri, data=json.dumps(data), **kwargs)

    def get_user_by_uid(self, user_uid, **kwargs):
        uri = "/api/User/{0}?idType=uid".format(user_uid)
        return self.get(uri, **kwargs)

    def get_user_by_username(self, username, **kwargs):
        uri = "/api/User/"
        params = {"username": username}
        return self.get(uri, params=params, **kwargs)

    def get_current_user(self, **kwargs):
        uri = "/api/User/my"
        return self.get(uri, **kwargs)

    def get_users(self, active=None, email=None, org_uid=None, user_uid=None, role_id=None, page_num=None,
                  page_size=None, **kwargs):
        uri = "/api/User"
        params = {"active": active, "userUid": user_uid, "email": email, "orgUid": org_uid, "roleId": role_id,
                  "pgNum": page_num, "pgSize": page_size}

        return self.get(uri, params=params, **kwargs)

    def block_user(self, user_id, **kwargs):
        uri = "/api/UserBlock/{0}".format(user_id)
        return self.put(uri, **kwargs)

    def unblock_user(self, user_id, **kwargs):
        uri = "/api/UserBlock/{0}".format(user_id)
        return self.delete(uri, **kwargs)

    def deactivate_user(self, user_id, block_user=None, **kwargs):
        uri = "/api/UserDeactivation/{0}".format(user_id)
        data = {"blockUser": block_user}
        return self.put(uri, data=json.dumps(data), **kwargs)

    def reactivate_user(self, user_id, unblock_user=None, **kwargs):
        uri = "/api/UserDeactivation/{0}".format(user_id)
        params = {"unblockUser": unblock_user}
        return self.delete(uri, params=params, **kwargs)

    def for_each_user(self, active=None, email=None, org_uid=None, username=None, user_uid=None, role_id=None,
                      then=None, return_each_page=False):
        func = self.get_users

        def for_each(response):
            util.for_each_api_item(response, func, 1000, then, "users", return_each_page)

        func(active=active, email=email, org_uid=org_uid, username=username, user_uid=user_uid, role_id=role_id,
             page_size=1000, then=for_each)
