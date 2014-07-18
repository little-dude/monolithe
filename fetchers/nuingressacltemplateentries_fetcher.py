# -*- coding: utf-8 -*-

from restnuage import NURESTFetcher


class NUIngressACLTemplateEntriesFetcher(NURESTFetcher):
    """ IngressACLTemplateEntry fetcher """

    @classmethod
    def managed_class(cls):
        """ Managed class """

        from .. import NUIngressACLTemplateEntry
        return NUIngressACLTemplateEntry