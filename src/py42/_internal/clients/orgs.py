import json

import py42.settings as settings
from py42._internal.base_classes import BaseClient
from py42._internal.clients.util import get_all_pages
from py42._internal.response import Py42Response


class OrgClient(BaseClient):
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
        return Py42Response(self._session.post(uri, data=json.dumps(data)))

    def get_by_id(self, org_id, **kwargs):
        uri = u"/api/Org/{0}".format(org_id)
        return Py42Response(self._session.get(uri, params=kwargs))

    def get_by_uid(self, org_uid, **kwargs):
        uri = u"/api/Org/{0}".format(org_uid)
        params = dict(idType=u"orgUid", **kwargs)
        return Py42Response(self._session.get(uri, params=params))

    def _get_page(self, page_num=None, page_size=None, **kwargs):
        uri = u"/api/Org"
        params = dict(pgNum=page_num, pgSize=page_size, **kwargs)
        return Py42Response(self._session.get(uri, params=params), json_key=u"orgs")

    def get_all(self, **kwargs):
        return get_all_pages(self._get_page, settings.items_per_page, u"orgs", **kwargs)

    def block(self, org_id):
        uri = u"/api/OrgBlock/{0}".format(org_id)
        return Py42Response(self._session.put(uri))

    def unblock(self, org_id):
        uri = u"/api/OrgBlock/{0}".format(org_id)
        return Py42Response(self._session.delete(uri))

    def deactivate(self, org_id):
        uri = u"/api/OrgDeactivation/{0}".format(org_id)
        return Py42Response(self._session.put(uri))

    def reactivate(self, org_id):
        uri = u"/api/OrgDeactivation/{0}".format(org_id)
        return Py42Response(self._session.delete(uri))

    def get_current(self, **kwargs):
        uri = u"/api/Org/my"
        return Py42Response(self._session.get(uri, params=kwargs))
