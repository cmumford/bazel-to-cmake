#!/usr/bin/env python3
# Copyright 2019 Google LLC
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

"""A script to convert Bazel build systems to CMakeLists.txt.

See README.md for more information.
"""


from bazel_to_cmake_lib import (
    BuildFileFunctions, Converter, WorkspaceFileFunctions)
import sys


def execfile(filepath, globals_=None, locals_=None):
    """A Python 3 equivalent to Python 2's execfile."""
    with open(filepath) as f:
        code = compile(f.read(), filepath, "exec")
        exec(code, globals_, locals_)


converter = Converter()


def GetDict(obj):
    ret = {}
    for k in dir(obj):
        if not k.startswith("_"):
            ret[k] = getattr(obj, k)
    return ret


globs = GetDict(converter)

execfile("WORKSPACE", GetDict(WorkspaceFileFunctions(converter)))
execfile("BUILD", GetDict(BuildFileFunctions(converter)))

with open(sys.argv[1], "w") as f:
    f.write(converter.convert())
