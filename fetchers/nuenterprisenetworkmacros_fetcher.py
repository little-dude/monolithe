# -*- coding: utf-8 -*-

from restnuage import NURESTFetcher


class NUEnterpriseNetworkMacrosFetcher(NURESTFetcher):
    """ EnterpriseNetworkMacro fetcher """

    @classmethod
    def managed_class(cls):
        """ Managed class """

        from .. import NUEnterpriseNetworkMacro
        return NUEnterpriseNetworkMacro