from ..shared.authentication import AuthenticationClient
from .. import sessionfactory


class StorageTargetedClient(AuthenticationClient):
    @classmethod
    def create_with_tmp_auth_from_plan_info(cls, storage_location_requester, plan_uid, destination_guid,
                                            is_async=False):
        session = sessionfactory.create_tmp_login_session_from_plan_info(storage_location_requester,
                                                                         plan_uid, destination_guid, is_async=is_async)
        return cls(session)
