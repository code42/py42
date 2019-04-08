from py42._internal.login_providers import C42ApiV1TokenProvider, C42ApiV3TokenProvider
from py42._internal.base_classes import BaseAuthStrategy
import py42._internal.session_factory as session_factory


class C42AuthorityAuthStrategy(BaseAuthStrategy):

    def create_v1_session(self, parent_session, *args, **kwargs):
        provider = C42ApiV1TokenProvider(parent_session)
        return session_factory.create_c42api_v1_session(provider, is_async=self._is_async)

    def create_jwt_session(self, parent_session, *args, **kwargs):
        provider = C42ApiV3TokenProvider(parent_session)
        return session_factory.create_c42api_v3_session(provider, is_async=self._is_async)

    def create_storage_session(self, c42_api_login_provider, *args, **kwargs):
        tmp = session_factory.create_c42api_tmp_storage_session(c42_api_login_provider, is_async=self._is_async)
        return self.create_v1_session(tmp)
