from py42.sdk.queries import BaseQuery


class FileEventQuery(BaseQuery):
    """Helper class for building V2 Code42 Forensic Search queries.

    A FileEventQuery instance's ``all()`` and ``any()`` take one or more
    :class:`~py42.sdk.queries.query_filter.FilterGroup` objects to construct a query that
    can be passed to the :meth:`FileEventService.search()` method. ``all()`` returns results
    that match all of the provided filter criteria, ``any()`` will return results that
    match any of the filters.

    For convenience, the :class:`FileEventQuery` constructor does the same as ``all()``.

    Usage example::

        email_filter = EmailSender.is_in(["test.user@example.com", "test.sender@example.com"])
        exposure_filter = ExposureType.exists()
        query = FileEventQuery.all(email_filter, exposure_filter)

    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.sort_key = "event.id"

    @property
    def version(self):
        return "v2"

    def __str__(self):
        groups_string = ",".join(
            str(group_item) for group_item in self._filter_group_list
        )
        if self.page_token is not None:
            paging_prop = f'"srtDir":"{self.sort_direction}", "srtKey":"{self.sort_key}", "pgToken":"{self.page_token}"'
        else:
            paging_prop = f'"srtDir":"{self.sort_direction}", "srtKey":"{self.sort_key}", "pgNum":{self.page_number}'
        json = f'{{"groupClause":"{self._group_clause}", "groups":[{groups_string}], {paging_prop}, "pgSize":{self.page_size}}}'
        return json

    def __iter__(self):
        filter_group_list = [dict(item) for item in self._filter_group_list]
        output_dict = {
            "groupClause": self._group_clause,
            "groups": filter_group_list,
            "pgSize": self.page_size,
            "srtDir": self.sort_direction,
            "srtKey": self.sort_key,
        }

        if self.page_token is not None:
            output_dict["pgToken"] = self.page_token
        else:
            output_dict["pgNum"] = self.page_number

        for key in output_dict:
            yield key, output_dict[key]
