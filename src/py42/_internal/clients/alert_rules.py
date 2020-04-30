import json

from py42._internal.clients.alertrules.cloud_share import CloudShareClient
from py42._internal.clients.alertrules.exfiltration import ExfiltrationClient
from py42._internal.clients.alertrules.file_type_mismatch import FileTypeMismatchClient
from py42.clients import BaseClient


class AlertRulesClient(BaseClient):
    """A client to manage Alert Rules."""

    _version = u"v1"
    _resource = u"Rules/"
    _api_prefix = u"/svc/api/{0}/{1}".format(_version, _resource)

    def __init__(self, session, user_context, detection_list_user_client):
        super(AlertRulesClient, self).__init__(session)
        self._user_context = user_context
        self._tenant_id = self._user_context.get_current_tenant_id()
        self._detection_list_user_client = detection_list_user_client
        self._exfiltration = None
        self._cloud_share = None
        self._file_type_mismatch = None

    @property
    def exfiltration(self):
        if not self._exfiltration:
            self._exfiltration = ExfiltrationClient(self._session, self._tenant_id)
        return self._exfiltration

    @property
    def cloudshare(self):
        if not self._cloud_share:
            self._cloud_share = CloudShareClient(self._session, self._tenant_id)
        return self._cloud_share

    @property
    def filetypemismatch(self):
        if not self._file_type_mismatch:
            self._file_type_mismatch = FileTypeMismatchClient(self._session, self._tenant_id)
        return self._file_type_mismatch

    def add_user(self, rule_id, user_id):
        """Update alert rule to monitor user aliases against the Uid for the given rule id.

        Args:
            rule_id (str): Observer Id of a rule to be updated.
            user_id (str): The Code42 userUid  of the user to add to the alert

        Returns
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        user_details = self._detection_list_user_client.get_by_id(user_id)
        user_aliases = user_details["cloudUsernames"] or []
        data = {
            u"tenantId": tenant_id,
            u"ruleId": rule_id,
            u"userList": [{u"userIdFromAuthority": user_id, u"userAliasList": user_aliases,}],
        }
        uri = u"{0}{1}".format(self._api_prefix, u"add-users")
        return self._session.post(uri, data=json.dumps(data))

    def remove_user(self, rule_id, user_id):
        """Update alert rule criteria to remove a user and all its aliases from a rule.

        Args:
            rule_id (str): Observer rule Id of a rule to be updated.
            user_id (str): The Code42 userUid  of the user to remove from the alert

        Returns
            :class:`py42.response.Py42Response`
        """
        user_ids = [user_id]
        tenant_id = self._user_context.get_current_tenant_id()
        data = {u"tenantId": tenant_id, u"ruleId": rule_id, u"userIdList": user_ids}
        uri = u"{0}{1}".format(self._api_prefix, u"remove-users")
        return self._session.post(uri, data=json.dumps(data))

    def remove_all_users(self, rule_id):
        """Update alert rule criteria to remove all users the from the alert rule.

        Args:
            rule_id (str): Observer rule Id of a rule to be updated.

        Returns
            :class:`py42.response.Py42Response`
        """
        tenant_id = self._user_context.get_current_tenant_id()
        data = {u"tenantId": tenant_id, u"ruleId": rule_id}
        uri = u"{0}{1}".format(self._api_prefix, u"remove-all-users")
        return self._session.post(uri, data=json.dumps(data))
