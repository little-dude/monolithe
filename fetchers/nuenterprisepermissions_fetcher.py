# -*- coding: utf-8 -*-

from restnuage import NURESTFetcher


class NUEnterprisePermissionsFetcher(NURESTFetcher):
    """ EnterprisePermission fetcher """

    @classmethod
    def managed_class(cls):
        """ Managed class """

        from .. import NUEnterprisePermission
        return NUEnterprisePermission