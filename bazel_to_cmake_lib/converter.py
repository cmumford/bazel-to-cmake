#!/usr/bin/env python3
# Copyright 2022 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import jinja2
import os

from .build_file_functions import BuildFileFunctions
from .workspace_file_functions import WorkspaceFileFunctions

this_dir = os.path.abspath(os.path.dirname(__file__))


def GetDict(obj):
    ret = {}
    for k in dir(obj):
        if not k.startswith("_"):
            ret[k] = getattr(obj, k)
    return ret


def execfile(filepath, globals_=None, locals_=None):
    """A Python 3 equivalent to Python 2's execfile."""
    with open(filepath) as f:
        code = compile(f.read(), filepath, "exec")
        exec(code, globals_, locals_)


class Converter(object):
    def __init__(self):
        self.prelude = ""
        self.toplevel = ""
        self.if_lua = ""

    def LoadCMakeTemplate(self):
        templateLoader = jinja2.FileSystemLoader(searchpath=this_dir)
        templateEnv = jinja2.Environment(loader=templateLoader)
        return templateEnv.get_template('cmake_template.txt')

    def convert(self):
        t = self.LoadCMakeTemplate()
        return t.render(prelude=self.prelude, toplevel=self.toplevel)

    def ConvertDir(self, cmake_out_file):
        if os.path.exists("WORKSPACE.bazel"):
            execfile("WORKSPACE.bazel", GetDict(WorkspaceFileFunctions(self)))
        elif os.path.exists("WORKSPACE"):
            execfile("WORKSPACE", GetDict(WorkspaceFileFunctions(self)))
        if os.path.exists("BUILD.bazel"):
            execfile("BUILD.bazel", GetDict(BuildFileFunctions(self)))
        if os.path.exists("BUILD"):
            execfile("BUILD", GetDict(BuildFileFunctions(self)))

        with open(cmake_out_file, "w") as f:
            f.write(self.convert())
