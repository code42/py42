class UserContext(object):
    """An object representing the currently logged in user."""

    def __init__(self, administration_client):
        self._administration_client = administration_client
        self._tenant_id = None

    def get_current_tenant_id(self):
        """Gets the currently signed in user's tenant ID."""
        if self._tenant_id is None:
            self._tenant_id = self._get_tenant_id()
        return self._tenant_id

    def _get_tenant_id(self):
        response = self._administration_client.get_current_tenant()
        return response[u"tenantUid"]
