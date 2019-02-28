from py42 import util
from py42.clients.authority.authority_base import AuthorityTargetedClient


class UserClient(AuthorityTargetedClient):

    def for_each_user(self, active=None, org_uid=None, then=None, return_each_page=False):
        func = self.get_users

        def for_each(response):
            util.for_each_api_item(response, func, 1000, then, "users", return_each_page)

        func(active=active, org_uid=org_uid, page_size=1000, then=for_each)

    def get_users(self, active=None, email=None, org_uid=None, username=None, user_uid=None,
                  role_id=None, page_num=None, page_size=None, **kwargs):
        uri = "/api/User"
        params = {"active": active, "username": username, "userUid": user_uid, "email": email,
                  "orgUid": org_uid, "roleId": role_id, "pgNum": page_num, "pgSize": page_size}

        return self.get(uri, params=params, **kwargs)

    def get_current_user(self, **kwargs):
        uri = "/api/User/my"
        return self.get(uri, **kwargs)
