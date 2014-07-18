# -*- coding: utf-8 -*-

from restnuage import NURESTFetcher


class NUVPortTagsFetcher(NURESTFetcher):
    """ VPortTag fetcher """

    @classmethod
    def managed_class(cls):
        """ Managed class """

        from .. import NUVPortTag
        return NUVPortTag