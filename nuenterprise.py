# -*- coding: utf-8 -*-
from .autogenerates import NUEnterprise as AutoGenerate


class NUEnterprise(AutoGenerate):
    """ Represents a Enterprise object """

    def instanciate_domain(self, domain, domain_template, async=False, callback=None):
        """ Instanciate a domain
            :param domain: object to instanciate
            :param domain_template: template to intanciate from
            :param async: Make an sync or async HTTP request
            :param callback: Callback method called when async is set to true
        """

        domain.template_id = domain_template.id
        return self.add_child_entity(entity=domain, async=async, callback=callback)

    def instanciate_gateway(self, gateway, gateway_template, async=False, callback=None):
        """ Instanciate a gateway
            :param gateway: object to instanciate
            :param gateway_template: template to intanciate from
            :param async: Make an sync or async HTTP request
            :param callback: Callback method called when async is set to true
        """

        gateway.template_id = gateway_template.id
        return self.add_child_entity(entity=gateway, async=async, callback=callback)
