from py42 import settings
from py42.services import BaseService
from py42.services.util import get_all_pages
from py42.util import convert_datetime_to_timestamp_str


class AuditLogsService(BaseService):
    def get_page(self, page_num, page_size=None, **kwargs):

        uri = u"/rpc/search/search-audit-log"
        page_size = page_size or settings.items_per_page
        params = dict(
            page=page_num - 1,
            pageSize=page_size,
            dateRange=kwargs["date_range"],
            eventTypes=kwargs["event_types"],
            actorIds=kwargs["user_ids"],
            actorNames=kwargs["user_names"],
            actorIpAddresses=kwargs["user_ip_addresses"],
            affectedUserIds=kwargs["affected_user_ids"],
            affectedUserNames=kwargs["affected_user_names"],
        )
        params["type$"] = "audit_log::audit_log_queries.search_audit_log/1"
        return self._connection.post(uri, json=params,)

    def get_all(
        self,
        begin_time=None,
        end_time=None,
        event_types=None,
        user_ids=None,
        user_names=None,
        user_ip_addresses=None,
        affected_user_ids=None,
        affected_user_names=None,
    ):
        comma = u","
        event_types = event_types.split(comma) if event_types else []
        user_ids = user_ids.split(comma) if user_ids else []
        user_names = user_names.split(comma) if user_names else []
        user_ip_addresses = user_ip_addresses.split(comma) if user_ip_addresses else []
        affected_user_ids = affected_user_ids.split(comma) if affected_user_ids else []
        affected_user_names = (
            affected_user_names.split(comma) if affected_user_names else []
        )

        date_range = {}
        if begin_time:
            date_range["startTime"] = convert_datetime_to_timestamp_str(begin_time)
        if end_time:
            date_range["endTime"] = convert_datetime_to_timestamp_str(end_time)

        return get_all_pages(
            self.get_page,
            "events",
            date_range=date_range,
            event_types=event_types,
            user_ids=user_ids,
            user_names=user_names,
            user_ip_addresses=user_ip_addresses,
            affected_user_ids=affected_user_ids,
            affected_user_names=affected_user_names,
        )
