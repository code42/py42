import json

from py42._internal.base_classes import BaseAuthorityClient
from py42._internal.clients import util


class UserClient(BaseAuthorityClient):
    def create_user(
        self,
        org_uid,
        username,
        email=None,
        password=None,
        first_name=None,
        last_name=None,
        notes=None,
        **kwargs
    ):
        uri = u"/api/User"
        data = {
            u"orgUid": org_uid,
            u"username": username,
            u"email": email,
            u"password": password,
            u"firstName": first_name,
            u"lastName": last_name,
            u"notes": notes,
        }
        return self._default_session.post(uri, data=json.dumps(data), **kwargs)

    def get_user_by_uid(self, user_uid, **kwargs):
        uri = u"/api/User/{0}?idType=uid".format(user_uid)
        return self._default_session.get(uri, **kwargs)

    def get_user_by_username(self, username, **kwargs):
        uri = u"/api/User"
        params = {u"username": username}
        return self._default_session.get(uri, params=params, **kwargs)

    def get_current_user(self, **kwargs):
        uri = u"/api/User/my"
        return self._default_session.get(uri, **kwargs)

    def get_users(
        self,
        active=None,
        email=None,
        org_uid=None,
        user_uid=None,
        role_id=None,
        page_num=None,
        page_size=None,
        q=None,
        **kwargs
    ):
        uri = u"/api/User"
        params = {
            u"active": active,
            u"userUid": user_uid,
            u"email": email,
            u"orgUid": org_uid,
            u"roleId": role_id,
            u"pgNum": page_num,
            u"pgSize": page_size,
            u"q": q,
        }

        return self._default_session.get(uri, params=params, **kwargs)

    def block_user(self, user_id, **kwargs):
        uri = u"/api/UserBlock/{0}".format(user_id)
        return self._default_session.put(uri, **kwargs)

    def unblock_user(self, user_id, **kwargs):
        uri = u"/api/UserBlock/{0}".format(user_id)
        return self._default_session.delete(uri, **kwargs)

    def deactivate_user(self, user_id, block_user=None, **kwargs):
        uri = u"/api/UserDeactivation/{0}".format(user_id)
        data = {u"blockUser": block_user}
        return self._default_session.put(uri, data=json.dumps(data), **kwargs)

    def reactivate_user(self, user_id, unblock_user=None, **kwargs):
        uri = u"/api/UserDeactivation/{0}".format(user_id)
        params = {u"unblockUser": unblock_user}
        return self._default_session.delete(uri, params=params, **kwargs)

    def change_user_org_assignment(self, user_id, org_id, **kwargs):
        uri = u"/api/UserMoveProcess"
        data = {u"userId": user_id, u"parentOrgId": org_id}
        return self._default_session.post(uri, data=json.dumps(data), **kwargs)

    def for_each_user(
        self, active=None, email=None, org_uid=None, role_id=None, then=None, return_each_page=False
    ):
        func = self.get_users

        def for_each(response):
            util.for_each_api_item(response, func, 1000, then, u"users", return_each_page)

        func(
            active=active,
            email=email,
            org_uid=org_uid,
            role_id=role_id,
            page_size=1000,
            then=for_each,
        )
