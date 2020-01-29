import json

from py42._internal.base_classes import BaseAuthorityClient


class LegalHoldClient(BaseAuthorityClient):
    def create_legal_hold_policy(self, name, policy=None):
        uri = u"/api/v4/legal-hold-policy/create"
        data = {u"name": name, u"policy": policy}
        return self._default_session.post(uri, data=json.dumps(data))

    def create_legal_hold(
        self, name, hold_policy_uid, description=None, notes=None, hold_ext_ref=None
    ):
        uri = u"/api/LegalHold"
        data = {
            u"name": name,
            u"holdPolicyUid": hold_policy_uid,
            u"description": description,
            u"notes": notes,
            u"holdExtRef": hold_ext_ref,
        }
        return self._default_session.post(uri, data=json.dumps(data))

    def get_legal_hold_policy_by_uid(self, legal_hold_policy_uid):
        uri = u"/api/v4/legal-hold-policy/view"
        params = {u"legalHoldPolicyUid": legal_hold_policy_uid}
        return self._v3_required_session.get(uri, params=params)

    def get_all_legal_hold_policies(self):
        uri = u"/api/v4/legal-hold-policy/list"
        return self._v3_required_session.get(uri)

    def get_legal_hold_by_uid(self, legal_hold_uid):
        uri = u"/api/LegalHold/{0}".format(legal_hold_uid)
        return self._default_session.get(uri)

    def get_legal_holds(
        self,
        creator_user_uid=None,
        active_state=u"ACTIVE",
        name=None,
        hold_ext_ref=None,
        page_num=None,
        page_size=None,
        **kwargs
    ):
        uri = u"/api/LegalHold"
        params = {
            u"creatorUserUid": creator_user_uid,
            u"activeState": active_state,
            u"name": name,
            u"holdExtRef": hold_ext_ref,
            u"pgNum": page_num,
            u"pgSize": page_size,
        }
        return self._default_session.get(uri, params=params)

    def get_legal_hold_memberships(
        self,
        legal_hold_membership_uid=None,
        legal_hold_uid=None,
        user_uid=None,
        user=None,
        active_state=None,
        page_num=None,
        page_size=None,
    ):
        params = {
            u"legalHoldMembershipUid": legal_hold_membership_uid,
            u"legalHoldUid": legal_hold_uid,
            u"userUid": user_uid,
            u"user": user,
            u"activeState": active_state,
            u"pgNum": page_num,
            u"pgSize": page_size,
        }
        uri = u"/api/LegalHoldMembership"
        return self._default_session.get(uri, params=params)

    def add_user_to_legal_hold(self, user_uid, legal_hold_uid):
        uri = u"/api/LegalHoldMembership"
        data = {u"legalHoldUid": legal_hold_uid, u"userUid": user_uid}
        return self._default_session.post(uri, data=json.dumps(data))

    def remove_user_from_legal_hold(self, legal_hold_membership_uid):
        uri = u"/api/LegalHoldMembershipDeactivation"
        data = {u"legalHoldMembershipUid": legal_hold_membership_uid}
        return self._default_session.post(uri, data=json.dumps(data))

    def deactivate_legal_hold(self, legal_hold_uid):
        uri = u"/api/v4/legal-hold-deactivation/update"
        data = {u"legalHoldUid": legal_hold_uid}
        return self._v3_required_session.post(uri, data=json.dumps(data))

    def reactivate_legal_hold(self, legal_hold_uid):
        uri = u"/api/LegalHoldReactivation/{0}".format(legal_hold_uid)
        return self._default_session.put(uri)
