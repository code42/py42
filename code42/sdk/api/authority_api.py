import json
from .handlers import V1AuthHandler, V3AuthHandler
from .handlers.http import GenericAPIClient, util


class AuthorityAPIClient(GenericAPIClient):

    def __init__(self, default_session, v3_session_if_default_not_v3=None):
        super(AuthorityAPIClient, self).__init__(default_session)
        if v3_session_if_default_not_v3 is not None:
            self.__v3_client = GenericAPIClient(v3_session_if_default_not_v3)
        else:
            self.__v3_client = self

    @classmethod
    def create_v3_token_client(cls, auth_session, is_async):
        handler = V3AuthHandler(auth_session)
        session = util.create_session(auth_session.host_address, handler, auth_session.proxies, is_async)
        return cls(session)

    @classmethod
    def create_v1_token_client(cls, auth_session, is_async):
        v3_handler = V3AuthHandler(auth_session)
        v3_session = util.create_session(auth_session.host_address, v3_handler, auth_session.proxies, is_async)
        v1_handler = V1AuthHandler(auth_session)
        v1_session = util.create_session(auth_session.host_address, v1_handler, auth_session.proxies, is_async)
        return cls(v1_session, v3_session)

    def wait(self):
        super(AuthorityAPIClient, self).wait()
        if self.__v3_client is not self:
            self.__v3_client.wait()

    def for_each_user(self, active=None, org_uid=None, then=None, **kwargs):
        func = self.get_users
        func(active=active, org_uid=org_uid, page_size=1000, then=util.for_each_api_item, obj_retriever=func,
             foreach_pg_size=1000, foreach_user_callback=then, foreach_datakey="users", **kwargs)

    def get_users(self, active=None, username=None, email=None, user_uid=None, org_uid=None,
                  role_id=None, page_num=None, page_size=None, **kwargs):

        uri = "/api/User"
        params = {"active": active, "username": username, "userUid": user_uid, "email": email,
                  "orgUid": org_uid, "roleId": role_id, "pgNum": page_num, "pgSize": page_size}

        return self.get(uri, params=params, **kwargs)

    def get_computers(self, page_num=None, page_size=None, active=None, include_backup_usage=None, **kwargs):
        uri = "/api/Computer"
        params = {"active": active, "pgNum": page_num, "pgSize": page_size, "incBackupUsage": include_backup_usage}

        return self.get(uri, params=params, **kwargs)

    def get_orgs(self, page_num=None, page_size=None, **kwargs):
        uri = "/api/Org"
        params = {"pgNum": page_num, "pgSize": page_size}

        return self.get(uri, params=params, **kwargs)

    def get_current_user(self, **kwargs):
        uri = "/api/User/my"
        return self.get(uri, **kwargs)

    def get_current_user_org(self, **kwargs):
        uri = "/api/Org/my"
        return self.get(uri, **kwargs)

    def get_security_event_locations(self, user_uid, **kwargs):
        uri = "/c42api/v3/SecurityEventsLocation"
        params = {"userUid": user_uid}

        return self.__v3_client.get(uri, params=params, **kwargs)

    def storage_auth_token(self, plan_uid, destination_guid, **kwargs):
        uri = "/api/StorageAuthToken"
        data = {"planUid": plan_uid, "destinationGuid": destination_guid}

        return self.post(uri, data=json.dumps(data), **kwargs)
