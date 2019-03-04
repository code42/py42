from py42.clients.authority import restore, administration, security, legalhold
from py42.clients.authority.authority_base import AuthorityTargetedClient


class AuthorityClient(AuthorityTargetedClient):

    def __init__(self, default_session, v3_required_session=None):
        super(AuthorityClient, self).__init__(default_session, v3_required_session)
        self._administration_client = administration.AdministrationClient(default_session)
        self._legal_hold_client = legalhold.LegalHoldClient(self._v3_required_session)
        self._restore_client = restore.RestoreClient(default_session)
        self._security_client = security.SecurityClient(self._v3_required_session)

    @property
    def administration(self):
        return self._administration_client

    @property
    def legal_hold(self):
        return self._legal_hold_client

    @property
    def restore(self):
        return self._restore_client

    @property
    def security(self):
        return self._security_client
