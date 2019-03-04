from py42.clients.authority.authority_base import AuthorityTargetedClient
import json


class LegalHoldClient(AuthorityTargetedClient):

    def create_legal_hold_policy(self, name, policy=None, **kwargs):
        uri = "/api/v4/legal-hold-policy/create"
        data = {"name": name, "policy": policy}
        return self.post(uri, data=json.dumps(data), **kwargs)

    def create_legal_hold(self, name, hold_policy_uid, description=None, notes=None, hold_ext_ref=None, **kwargs):
        uri = "/api/LegalHold"
        data = {"name": name, "holdPolicyUid": hold_policy_uid, "description": description, "notes": notes,
                "holdExtRef": hold_ext_ref}
        return self.post(uri, data=json.dumps(data), **kwargs)

    def get_legal_hold_policy_by_uid(self, legal_hold_policy_uid, **kwargs):
        uri = "/api/v4/legal-hold-policy/view"
        params = {"legalHoldPolicyUid": legal_hold_policy_uid}
        return self.get(uri, params=params, **kwargs)

    def get_all_legal_hold_policies(self, **kwargs):
        uri = "/api/v4/legal-hold-policy/list"
        return self.get(uri, **kwargs)

    def get_legal_hold_by_uid(self, legal_hold_uid, **kwargs):
        uri = "/api/LegalHold/{}".format(legal_hold_uid, **kwargs)
        return self.get(uri)

    def get_legal_holds(self, legal_hold_uid=None, creator_user_uid=None, active_state="ACTIVE", name=None,
                        hold_ext_ref=None, page_num=None, page_size=None, **kwargs):
        uri = "/api/LegalHold"
        params = {"legalHoldUid": legal_hold_uid, "creatorUserUid": creator_user_uid, "activeState": active_state,
                  "name": name, "holdExtRef": hold_ext_ref, "pgNum": page_num, "pgSize": page_size}
        return self.get(uri, params=params, **kwargs)

    def get_legal_hold_memberships(self, legal_hold_membership_uid=None, legal_hold_uid=None, user_uid=None, user=None,
                                   active_state=None, page_num=None, page_size=None, **kwargs):
        params = {"legalHoldMembershipUid": legal_hold_membership_uid, "legalHoldUid": legal_hold_uid,
                  "userUid": user_uid, "user": user, "activeState": active_state, "pgNum": page_num, "pgSize": page_size}
        uri = "/api/LegalHoldMembership"
        return self.get(uri, params=params, **kwargs)

    def add_user_to_legal_hold(self, user_uid, legal_hold_uid, **kwargs):
        uri = "/api/LegalHoldMembership"
        data = {"legalHoldUid": legal_hold_uid,
                "userUid": user_uid}
        return self.post(uri, data=json.dumps(data), **kwargs)

    def remove_user_from_legal_hold(self, legal_hold_membership_uid, **kwargs):
        uri = "/api/LegalHoldMembershipDeactivation"
        data = {"legalHoldMembershipUid": legal_hold_membership_uid}
        return self.post(uri, data=json.dumps(data), **kwargs)
