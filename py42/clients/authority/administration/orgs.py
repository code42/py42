from py42.clients.authority.authority_base import AuthorityTargetedClient


class OrgClient(AuthorityTargetedClient):

    def get_orgs(self, page_num=None, page_size=None, **kwargs):
        uri = "/api/Org"
        params = {"pgNum": page_num, "pgSize": page_size}

        return self.get(uri, params=params, **kwargs)

    def get_current_user_org(self, **kwargs):
        uri = "/api/Org/my"
        return self.get(uri, **kwargs)
