import json

from py42._internal.base_classes import BaseAuthorityClient
from py42._internal.clients.util import get_all_pages
import py42.settings as settings


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
        return self._default_session.post(uri, data=json.dumps(data))

    def get_user_by_id(self, user_id):
        uri = u"/api/User/{0}".format(user_id)
        return self._default_session.get(uri)

    def get_user_by_uid(self, user_uid):
        uri = u"/api/User/{0}?idType=uid".format(user_uid)
        return self._default_session.get(uri)

    def get_user_by_username(self, username):
        uri = u"/api/User"
        params = {u"username": username}
        return self._default_session.get(uri, params=params)

    def get_current_user(self):
        uri = u"/api/User/my"
        return self._default_session.get(uri)

    def _get_users_page(
        self,
        active=None,
        email=None,
        org_uid=None,
        role_id=None,
        page_num=None,
        page_size=None,
        q=None,
    ):
        uri = u"/api/User"
        params = {
            u"active": active,
            u"email": email,
            u"orgUid": org_uid,
            u"roleId": role_id,
            u"pgNum": page_num,
            u"pgSize": page_size,
            u"q": q,
        }

        return self._default_session.get(uri, params=params)

    def get_users(self, active=None, email=None, org_uid=None, role_id=None, q=None):
        return get_all_pages(
            self._get_users_page,
            settings.items_per_page,
            u"users",
            active=active,
            email=email,
            org_uid=org_uid,
            role_id=role_id,
            q=q,
        )

    def block_user(self, user_id):
        uri = u"/api/UserBlock/{0}".format(user_id)
        return self._default_session.put(uri)

    def unblock_user(self, user_id):
        uri = u"/api/UserBlock/{0}".format(user_id)
        return self._default_session.delete(uri)

    def deactivate_user(self, user_id, block_user=None):
        uri = u"/api/UserDeactivation/{0}".format(user_id)
        data = {u"blockUser": block_user}
        return self._default_session.put(uri, data=json.dumps(data))

    def reactivate_user(self, user_id, unblock_user=None):
        uri = u"/api/UserDeactivation/{0}".format(user_id)
        params = {u"unblockUser": unblock_user}
        return self._default_session.delete(uri, params=params)

    def change_user_org_assignment(self, user_id, org_id):
        uri = u"/api/UserMoveProcess"
        data = {u"userId": user_id, u"parentOrgId": org_id}
        return self._default_session.post(uri, data=json.dumps(data))
