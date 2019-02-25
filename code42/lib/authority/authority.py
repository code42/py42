from .administration import AdministrationClient
from .authoritybase import AuthorityTargetedClient
from .backuprestore import BackupRestoreClient
from .securitytools import SecurityToolsClient


class AuthorityClient(AuthorityTargetedClient):

    def __init__(self, default_session, v3_required_session=None):
        super(AuthorityClient, self).__init__(default_session, v3_required_session)
        self._administration = AdministrationClient(default_session)
        self._backuprestore = BackupRestoreClient(default_session)
        self._securitytools = SecurityToolsClient(self._v3_required_session)

    @property
    def administration(self):
        return self._administration

    @property
    def backuprestore(self):
        return self._backuprestore

    @property
    def securitytools(self):
        return self._securitytools
