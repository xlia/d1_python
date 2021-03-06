#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2013 DataONE
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""DataONE Test Utilities package
"""
from __future__ import absolute_import

import setuptools


def main():
  setuptools.setup(
    name='dataone.test_utilities',
    version='2.4.2',
    description='Utilities for testing DataONE infrastructure components',
    author='DataONE Project',
    author_email='developers@dataone.org',
    url='https://github.com/DataONEorg/d1_python',
    license='Apache License, Version 2.0',
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
      'dataone.libclient == 2.4.2',
      #
      'contextlib2 == 0.5.5',
      'coverage == 4.5.1',
      'coveralls == 1.2.0',
      'decorator == 4.2.1',
      'freezegun == 0.3.9',
      'mock == 2.0.0',
      'multi-mechanize == 1.2.0',
      'posix-ipc == 1.0.4',
      'psutil == 5.4.3',
      'pyasn1 == 0.4.2',
      'pytest == 3.4.0',
      'pytest-cov == 2.5.1',
      'pytest-django == 3.1.2',
      'pytest-forked == 0.2',
      'pytest-xdist == 1.22.0',
      'pyxb == 1.2.6',
      'rdflib == 4.2.2',
      'requests == 2.18.4',
      'responses == 0.8.1',
    ],
    setup_requires=[
      'setuptools_git >= 1.1',
    ],
    classifiers=[
      'Development Status :: 5 - Production/Stable',
      'Intended Audience :: Developers',
      'Topic :: Scientific/Engineering',
      'License :: OSI Approved :: Apache Software License',
      'Programming Language :: Python :: 2',
      'Programming Language :: Python :: 2.7',
    ],
    keywords=(
      'DataONE source code unit tests ingeration tests coverage travis '
      'coveralls'
    ),
  )


if __name__ == '__main__':
  main()
