# -*- coding: utf-8 -*-

from restnuage import NURESTFetcher


class NUAlarmsFetcher(NURESTFetcher):
    """ Alarm fetcher """

    @classmethod
    def managed_class(cls):
        """ Managed class """

        from .. import NUAlarm
        return NUAlarm