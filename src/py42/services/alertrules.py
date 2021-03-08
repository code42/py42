from py42.exceptions import Py42InvalidRuleError
from py42.exceptions import Py42NotFoundError
from py42.services import BaseService


class AlertRulesService(BaseService):
    """A service to manage Alert Rules."""

    _api_prefix = u"/svc/api/v1/Rules/"

    def __init__(self, connection, user_context, user_profile_service):
        super(AlertRulesService, self).__init__(connection)
        self._user_context = user_context
        self._user_profile_service = user_profile_service
        self._exfiltration = None
        self._cloud_share = None
        self._file_type_mismatch = None

    @property
    def exfiltration(self):
        if not self._exfiltration:
            tenant_id = self._user_context.get_current_tenant_id()
            self._exfiltration = ExfiltrationService(self._connection, tenant_id)
        return self._exfiltration

    @property
    def cloudshare(self):
        if not self._cloud_share:
            tenant_id = self._user_context.get_current_tenant_id()
            self._cloud_share = CloudShareService(self._connection, tenant_id)
        return self._cloud_share

    @property
    def filetypemismatch(self):
        if not self._file_type_mismatch:
            tenant_id = self._user_context.get_current_tenant_id()
            self._file_type_mismatch = FileTypeMismatchService(
                self._connection, tenant_id
            )
        return self._file_type_mismatch

    def add_user(self, rule_id, user_id):
        tenant_id = self._user_context.get_current_tenant_id()
        user_details = self._user_profile_service.get_by_id(user_id)
        user_aliases = user_details.data.get(u"cloudUsernames") or []
        data = {
            u"tenantId": tenant_id,
            u"ruleId": rule_id,
            u"userList": [
                {u"userIdFromAuthority": user_id, u"userAliasList": user_aliases}
            ],
        }
        uri = u"{}{}".format(self._api_prefix, u"add-users")
        try:
            return self._connection.post(uri, json=data)
        except Py42NotFoundError as err:
            raise Py42InvalidRuleError(err, rule_id)

    def remove_user(self, rule_id, user_id):
        user_ids = [user_id]
        tenant_id = self._user_context.get_current_tenant_id()
        data = {u"tenantId": tenant_id, u"ruleId": rule_id, u"userIdList": user_ids}
        uri = u"{}{}".format(self._api_prefix, u"remove-users")
        return self._connection.post(uri, json=data)

    def remove_all_users(self, rule_id):
        tenant_id = self._user_context.get_current_tenant_id()
        data = {u"tenantId": tenant_id, u"ruleId": rule_id}
        uri = u"{}{}".format(self._api_prefix, u"remove-all-users")
        return self._connection.post(uri, json=data)


class CloudShareService(BaseService):
    _endpoint = u"/svc/api/v1/Rules/query-cloud-share-permissions-rule"

    def __init__(self, connection, tenant_id):
        super(CloudShareService, self).__init__(connection)
        self._tenant_id = tenant_id

    def get(self, rule_id):
        """Fetch cloud share alert rule by rule id.

        Args:
            rule_id (str): Observer rule Id of a rule to be fetched.

        Returns
            :class:`py42.response.Py42Response`
        """
        data = {u"tenantId": self._tenant_id, u"ruleIds": [rule_id]}
        return self._connection.post(self._endpoint, json=data)


class ExfiltrationService(BaseService):
    _endpoint = u"/svc/api/v1/Rules/query-endpoint-exfiltration-rule"

    def __init__(self, connection, tenant_id):
        super(ExfiltrationService, self).__init__(connection)
        self._tenant_id = tenant_id

    def get(self, rule_id):
        """Fetch exfiltration alert rule by rule id.

        Args:
            rule_id (str): Observer rule Id of a rule to be fetched.

        Returns
            :class:`py42.response.Py42Response`
        """
        data = {u"tenantId": self._tenant_id, u"ruleIds": [rule_id]}
        return self._connection.post(self._endpoint, json=data)


class FileTypeMismatchService(BaseService):
    _endpoint = u"/svc/api/v1/Rules/query-file-type-mismatch-rule"

    def __init__(self, connection, tenant_id):
        super(FileTypeMismatchService, self).__init__(connection)
        self._tenant_id = tenant_id

    def get(self, rule_id):
        """Fetch File type mismatch alert rules by rule id.

        Args:
            rule_id (str): Observer rule Id of a rule to be fetched.

        Returns
            :class:`py42.response.Py42Response`
        """
        data = {u"tenantId": self._tenant_id, u"ruleIds": [rule_id]}
        return self._connection.post(self._endpoint, json=data)
