import json

from py42._internal.base_classes import BaseAuthorityClient
from py42._internal.clients.util import get_all_pages
import py42.settings as settings


class OrgClient(BaseAuthorityClient):
    def create_org(
        self, org_name, org_ext_ref=None, notes=None, parent_org_uid=None, classification=None
    ):
        uri = u"/api/Org/"
        data = {
            u"orgName": org_name,
            u"orgExtRef": org_ext_ref,
            u"notes": notes,
            u"parentOrgUid": parent_org_uid,
            u"classification": classification,
        }
        return self._default_session.post(uri, data=json.dumps(data))

    def get_org_by_id(self, org_id):
        uri = u"/api/Org/{0}".format(org_id)
        return self._default_session.get(uri)

    def get_org_by_uid(self, org_uid):
        uri = u"/api/Org/{0}?idType=orgUid".format(org_uid)
        return self._default_session.get(uri)

    def _get_orgs_page(self, page_num=None, page_size=None):
        uri = u"/api/Org"
        params = {u"pgNum": page_num, u"pgSize": page_size}

        return self._default_session.get(uri, params=params)

    def get_orgs(self):
        return get_all_pages(self._get_orgs_page, settings.items_per_page, u"orgs")

    def block_org(self, org_id):
        uri = u"/api/OrgBlock/{0}".format(org_id)
        return self._default_session.put(uri)

    def unblock_org(self, org_id):
        uri = u"/api/OrgBlock/{0}".format(org_id)
        return self._default_session.delete(uri)

    def deactivate_org(self, org_id):
        uri = u"/api/OrgDeactivation/{0}".format(org_id)
        return self._default_session.put(uri)

    def reactivate_org(self, org_id):
        uri = u"/api/OrgDeactivation/{0}".format(org_id)
        return self._default_session.delete(uri)

    def get_current_user_org(self):
        uri = u"/api/Org/my"
        return self._default_session.get(uri)
