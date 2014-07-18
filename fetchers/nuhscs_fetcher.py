# -*- coding: utf-8 -*-

from restnuage import NURESTFetcher


class NUHSCsFetcher(NURESTFetcher):
    """ HSC fetcher """

    @classmethod
    def managed_class(cls):
        """ Managed class """

        from .. import NUHSC
        return NUHSC