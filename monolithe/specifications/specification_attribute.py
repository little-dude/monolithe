# -*- coding: utf-8 -*-
#
# Copyright (c) 2015, Alcatel-Lucent Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its contributors
#       may be used to endorse or promote products derived from this software without
#       specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
# ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
# (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
# ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
# SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import json
import pkgutil

from copy import deepcopy

from monolithe.lib import SDKUtils


class SpecificationAttribute(object):
    """ Define an attribute of an object

    """
    def __init__(self, specification, data=None):
        """ Define an attribute

            Example:
                remote_name: associatedGatewayID
                local_name: associated_gateway_id
                local_type: str
        """
        self.specification = specification

        # Main attributes
        self.description = None
        self._remote_name = None
        self.local_name = None
        self.local_type = None
        self.has_time_attribute = False

        # Other attributes
        self.channel = None
        self.allowed_chars = None
        self.allowed_choices = None
        self.autogenerated = False
        self.availability = None
        self.creation_only = False
        self.default_order = False
        self.default_value = None
        self.deprecated = False
        self.filterable = True
        self.format = "free"
        self.max_length = None
        self.max_value = None
        self.min_length = None
        self.min_value = None
        self.orderable = True
        self.read_only = False
        self.required = False
        self.unique = False
        self.unique_scope = None
        self._type = None
        self.exposed = True
        self.transient = False

        # Load information from data
        if data:
            self.from_dict(data)

    @property
    def type(self):
        """
        """
        return self._type

    @type.setter
    def type(self, value):
        """
        """
        self._type = value

        if value:
            self.local_type = SDKUtils.get_python_type_name(type_name=value)
            if self.local_type == "time":
                self.has_time_attribute = True

    @property
    def remote_name(self):
        """
        """
        return self._remote_name

    @remote_name.setter
    def remote_name(self, value):
        """
        """
        self._remote_name = value
        if self.specification and self.specification.monolithe_config:
            self.local_name = SDKUtils.get_python_name(self.specification.monolithe_config.map_attribute(self.specification.remote_name, value))
        else:
            self.local_name = value

    def from_dict(self, data):
        """

        """
        try:
            self.remote_name = data["name"]
            self.allowed_chars = data["allowed_chars"]
            self.allowed_choices = data["allowed_choices"]
            self.autogenerated = data["autogenerated"]
            self.channel = data["channel"]
            self.creation_only = data["creation_only"]
            self.default_order = data["default_order"]
            self.deprecated = data["deprecated"] if "deprecated" in data else False
            self.description = data["description"]
            self.exposed = data["exposed"] if "exposed" in data else True
            self.filterable = data["filterable"]
            self.format = data["format"]
            self.max_length = data["max_length"]
            self.max_value = data["max_value"]
            self.min_length = data["min_length"]
            self.min_value = data["min_value"]
            self.orderable = data["orderable"]
            self.read_only = data["read_only"]
            self.required = data["required"]
            self.transient = data["transient"] if "transient" in data else False
            self.type = data["type"]
            self.unique = data["unique"]
            self.unique_scope = data["uniqueScope"] if "uniqueScope" in data else None
        except Exception as ex:
            raise Exception("Unable to parse attribute %s for specification %s: %s" % (data["name"], self.specification.remote_name, ex))

    def to_dict(self):
        """ Transform an attribute to a dict
        """
        data = {}

        data["allowed_chars"] = self.allowed_chars
        data["allowed_choices"] = self.allowed_choices
        data["autogenerated"] = self.autogenerated
        data["channel"] = self.channel
        data["creation_only"] = self.creation_only
        data["default_order"] = self.default_order
        data["deprecated"] = self.deprecated
        data["description"] = self.description
        data["exposed"] = self.exposed
        data["filterable"] = self.filterable
        data["format"] = self.format
        data["max_length"] = self.max_length
        data["max_value"] = self.max_value
        data["min_length"] = self.min_length
        data["min_value"] = self.min_value
        data["name"] = self.remote_name
        data["orderable"] = self.orderable
        data["read_only"] = self.read_only
        data["required"] = self.required
        data["transient"] = self.transient
        data["type"] = self.type
        data["unique"] = self.unique
        data["uniqueScope"] = self.unique_scope

        return data
