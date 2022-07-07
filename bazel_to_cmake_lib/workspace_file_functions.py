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

class WorkspaceFileFunctions(object):
    def __init__(self, converter):
        self.converter = converter

    def load(self, *args):
        pass

    def workspace(self, **kwargs):
        self.converter.prelude += "project(%s)\n" % (kwargs["name"])

    def http_archive(self, **kwargs):
        pass

    def git_repository(self, **kwargs):
        pass
