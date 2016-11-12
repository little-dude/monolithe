# -*- coding: utf-8 -*-
#
# Copyright (c) 2015-2016, Alcatel-Lucent Inc
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above copyright
#       notice, this list of conditions and the following disclaimer in the
#       documentation and/or other materials provided with the distribution.
#     * Neither the name of the copyright holder nor the names of its
#       contributors may be used to endorse or promote products derived from
#       this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

from future import standard_library
standard_library.install_aliases()

from configparser import RawConfigParser

from monolithe.lib import TaskManager
from monolithe.generators.lib import TemplateFileWriter


class APIVersionWriter(TemplateFileWriter):

    def __init__(self, monolithe_config, api_info):
        package = "monolithe.generators.lang.rust"
        super(APIVersionWriter, self).__init__(package=package)

        self.monolithe_config = monolithe_config

        self.api_version = api_info["version"]
        self.api_root = api_info["root"]
        self.api_prefix = api_info["prefix"]

        get_config = self.monolithe_config.get_option
        self._output = get_config("output", "transformer")
        self._transformation_name = get_config("name", "transformer")
        self._product_accronym = get_config("product_accronym")
        self._product_name = get_config("product_name")

        self.output = "%s/rust/" % self._output

        self.attrs_defaults = RawConfigParser()
        path = "%s/__attributes_defaults/attrs_defaults.ini" % self.output
        self.attrs_defaults.optionxform = str
        self.attrs_defaults.read(path)

        with open("%s/__code_header" % self.output, "r") as f:
            self.header_content = f.read()

    def perform(self, specifications):
        """
        """

        task_manager = TaskManager()
        for rest_name, specification in specifications.items():
            task_manager.start_task(
                method=self._write_model,
                specification=specification,
                specification_set=specifications)

        task_manager.wait_until_exit()
        self._write_info(specifications.values())

    def _write_model(self, specification, specification_set):
        defaults = {}
        section = specification.entity_name
        if self.attrs_defaults.has_section(section):
            for attribute in self.attrs_defaults.options(section):
                defaults[attribute] = self.attrs_defaults.get(section, attribute)

        # in rust structs cannot have attributes named "type" because it's a
        # reserved keyword, so we rename such attributes to "type_".
        for attribute in specification.attributes:
            if attribute.name == "type":
                attribute.local_name = "type_"

        self.write(destination="%s/src" % self.output,
                   filename="%s.rs" % (specification.entity_name.lower()),
                   template_name="model.rs.tpl",
                   specification=specification,
                   specification_set=specification_set,
                   header=self.header_content,
                   attribute_defaults=defaults)

    def _write_info(self, specifications):
        self.write(destination="%s/src" % self.output,
                   filename="lib.rs",
                   template_name="lib.rs.tpl",
                   specifications=specifications,
                   header=self.header_content)
