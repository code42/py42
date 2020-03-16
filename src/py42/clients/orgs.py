import json

from py42.clients import BaseClient
from py42.clients.util import get_all_pages


class OrgClient(BaseClient):
    def create_org(
        self, org_name, org_ext_ref=None, notes=None, parent_org_uid=None, classification=None
    ):
        """[summary]
        
        Args:
            BaseClient ([type]): [description]
            org_name ([type]): [description]
            org_ext_ref ([type], optional): [description]. Defaults to None.
            notes ([type], optional): [description]. Defaults to None.
            parent_org_uid ([type], optional): [description]. Defaults to None.
            classification ([type], optional): [description]. Defaults to None.
        
        Returns:
            [type]: [description]
        """
        uri = u"/api/Org/"
        data = {
            u"orgName": org_name,
            u"orgExtRef": org_ext_ref,
            u"notes": notes,
            u"parentOrgUid": parent_org_uid,
            u"classification": classification,
        }
        return self._session.post(uri, data=json.dumps(data))

    def get_by_id(self, org_id, **kwargs):
        """[summary]
        
        Returns:
            [type]: [description]
        """
        uri = u"/api/Org/{0}".format(org_id)
        return self._session.get(uri, params=kwargs)

    def get_by_uid(self, org_uid, **kwargs):
        """[summary]
        
        Args:
            org_uid ([type]): [description]
        
        Returns:
            [type]: [description]
        """
        uri = u"/api/Org/{0}".format(org_uid)
        params = dict(idType=u"orgUid", **kwargs)
        return self._session.get(uri, params=params)

    def _get_page(self, page_num=None, page_size=None, **kwargs):
        uri = u"/api/Org"
        params = dict(pgNum=page_num, pgSize=page_size, **kwargs)
        return self._session.get(uri, params=params)

    def get_all(self, **kwargs):
        """[summary]
        
        Returns:
            [type]: [description]
        """
        return get_all_pages(self._get_page, u"orgs", **kwargs)

    def block(self, org_id):
        """[summary]
        
        Args:
            org_id ([type]): [description]
        
        Returns:
            [type]: [description]
        """
        uri = u"/api/OrgBlock/{0}".format(org_id)
        return self._session.put(uri)

    def unblock(self, org_id):
        """[summary]
        
        Args:
            org_id ([type]): [description]
        
        Returns:
            [type]: [description]
        """
        uri = u"/api/OrgBlock/{0}".format(org_id)
        return self._session.delete(uri)

    def deactivate(self, org_id):
        """[summary]
        
        Args:
            org_id ([type]): [description]
        
        Returns:
            [type]: [description]
        """
        uri = u"/api/OrgDeactivation/{0}".format(org_id)
        return self._session.put(uri)

    def reactivate(self, org_id):
        """[summary]
        
        Args:
            org_id ([type]): [description]
        
        Returns:
            [type]: [description]
        """
        uri = u"/api/OrgDeactivation/{0}".format(org_id)
        return self._session.delete(uri)

    def get_current(self, **kwargs):
        """[summary]
        
        Returns:
            [type]: [description]
        """
        uri = u"/api/Org/my"
        return self._session.get(uri, params=kwargs)
