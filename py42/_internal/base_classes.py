class BaseAuthorityClient(object):
    def __init__(self, default_session, v3_required_session):
        self._default_session = default_session
        self._v3_required_session = v3_required_session


class BaseStorageClient(object):
    def __init__(self, session):
        self._session = session


class BaseAuthStrategy(object):
    def __init__(self, is_async=False):
        self._is_async = is_async

    def create_v1_session(self, *args, **kwargs):
        pass

    def create_jwt_session(self, *args, **kwargs):
        pass

    def create_storage_session(self, *args, **kwargs):
        pass


class BaseArchiveLocatorFactory(object):

    def create_security_archive_locators(self, *args, **kwargs):
        pass

    def create_backup_archive_locator(self, *args, **kwargs):
        pass
