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

import os
from pathlib import Path
import shutil
import subprocess
import unittest
from .converter import (Converter)

this_dir = os.path.abspath(os.path.dirname(__file__))
root_dir = Path(this_dir).parent.absolute()


class TestConverter(unittest.TestCase):

    cmake_project_file = 'CMakeLists.txt'
    cmake_build_dir = 'build_cmake'
    project_names = ['hello1', 'libsum']

    @staticmethod
    def GetAbsProjectDir(project_name):
        return os.path.join(root_dir, 'test', 'projects', project_name)

    @staticmethod
    def CleanBazelFiles(project_dir):
        cmd = ['bazel', 'clean']
        subprocess.check_call(cmd, cwd=project_dir)

    @staticmethod
    def CleanCMakeFiles(project_dir):
        abs_build_dir = os.path.join(
            project_dir, TestConverter.cmake_build_dir)
        shutil.rmtree(abs_build_dir, ignore_errors=True)
        abs_build_file = os.path.join(
            project_dir, TestConverter.cmake_project_file)
        if os.path.exists(abs_build_file):
            os.unlink(abs_build_file)

    @staticmethod
    def CleanProjectFiles():
        for project_dir in TestConverter.project_names:
            abs_project_dir = TestConverter.GetAbsProjectDir(project_dir)
            TestConverter.CleanBazelFiles(abs_project_dir)
            TestConverter.CleanCMakeFiles(abs_project_dir)

    @staticmethod
    def DoBazelBuild(project_dir):
        cmd = ['bazel', 'build']
        subprocess.check_call(cmd, cwd=project_dir)

    @staticmethod
    def DoCMakeBuild(project_dir):
        abs_build_dir = os.path.join(
            project_dir, TestConverter.cmake_build_dir)
        os.mkdir(abs_build_dir)
        cmd = ['cmake', '..']
        subprocess.check_call(cmd, cwd=abs_build_dir)
        cmd = ['cmake', '--build', '.']
        subprocess.check_call(cmd, cwd=abs_build_dir)

    @staticmethod
    def ConvertAndBuild(project_dir):
        abs_project_dir = TestConverter.GetAbsProjectDir(project_dir)

        # First build the Bazel project to validate it.
        TestConverter.DoBazelBuild(abs_project_dir)

        # TODO: Decouple Converter from current working directory.
        os.chdir(abs_project_dir)
        converter = Converter()
        converter.ConvertDir(TestConverter.cmake_project_file)

        # Build the converted CMake project.
        TestConverter.DoCMakeBuild(abs_project_dir)

    def setUp(self):
        TestConverter.CleanProjectFiles()

    def tearDown(self):
        TestConverter.CleanProjectFiles()

    def test_hello_world1(self):
        project_dir = 'hello1'
        TestConverter.ConvertAndBuild(project_dir)
        # Execute the CMake built output to verify correctly built.
        abs_project_dir = TestConverter.GetAbsProjectDir(project_dir)
        abs_exe = os.path.join(
            abs_project_dir, TestConverter.cmake_build_dir, 'hello-world')
        subprocess.check_call([abs_exe])

    def test_libsum(self):
        project_dir = 'libsum'
        TestConverter.ConvertAndBuild(project_dir)
        # Execute the CMake built output to verify correctly built.
        abs_project_dir = TestConverter.GetAbsProjectDir(project_dir)
        abs_lib = os.path.join(
            abs_project_dir, TestConverter.cmake_build_dir, 'libsum.a')
        self.assertTrue(os.path.exists(abs_lib))


if __name__ == '__main__':
    unittest.main()
