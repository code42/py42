from .http.authhandling import SecretProvider


class JWTTokenProvider(SecretProvider):
    def __init__(self, jwt_token_requester):
        self._jwt_token_requester = jwt_token_requester

    def get_secret(self):
        try:
            return self._jwt_token_requester.get_jwt_token_value()
        except Exception as e:
            message = "Failed to retrieve jwt token"
            raise Exception(message + ", caused by: " + e.message)


class V1TokenProvider(SecretProvider):
    def __init__(self, v1_token_requester):
        self._v1_token_requester = v1_token_requester

    def get_secret(self):
        try:
            return self._v1_token_requester.get_v1_token_value()
        except Exception as e:
            message = "Failed to retrieve v1 token"
            raise Exception(message + ", caused by: " + e.message)


class TmpStorageTokenProvider(SecretProvider):
    def __init__(self, storage_location_requester, plan_uid, destination_guid):
        self._storage_location_requester = storage_location_requester
        self._plan_uid = plan_uid
        self._destination_guid = destination_guid
        self._updated_info_needed = True
        self._logon_info = self.get_storage_logon_info()

    def get_storage_logon_info(self):
        try:
            if self._updated_info_needed:
                self._logon_info = self._storage_location_requester.get_storage_logon_info(self._plan_uid,
                                                                                           self._destination_guid)
                self._updated_info_needed = False

            return self._logon_info
        except Exception as e:
            message = "Failed to retrieve storage logon info"
            raise Exception(message + ", caused by: " + e.message)

    def get_secret(self):
        self._updated_info_needed = True
        logon_info = self.get_storage_logon_info()
        tmp_token = logon_info.get("loginToken")

        return tmp_token
