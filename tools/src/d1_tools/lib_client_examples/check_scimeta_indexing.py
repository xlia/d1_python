#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2016 DataONE
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
"""Check if a science metadata object can be successfully indexed by the CN

Submit a science object to CNDiagnostic.echoIndexedObject() and print the
result.

This is intended for checking only the science metadata object. However,
echoIndexedObject() also requires a System Metadata object, so one is
automatically generated and included in the request.

API:

CNDiagnostic.echoIndexedObject(session, queryEngine, sysmeta, object) → OctetStream
https://releases.dataone.org/online/api-documentation-v2.0.1/apis/CN_APIs.html
  #CNDiagnostic.echoIndexedObject
"""

from __future__ import absolute_import
from __future__ import print_function

import argparse
import StringIO

import d1_common.const
import d1_common.util
import d1_common.xml

import d1_test.instance_generator.system_metadata as gen_sysmeta

import d1_client.cnclient_2_0

DEFAULT_FORMAT_ID = 'http://www.isotc211.org/2005/gmd'


def main():
  parser = argparse.ArgumentParser(
    description=__doc__,
    formatter_class=argparse.RawDescriptionHelpFormatter,
  )
  parser.add_argument('path', help='Path to science metadata file')
  parser.add_argument(
    '--debug', action='store_true', help='Debug level logging'
  )

  args = parser.parse_args()

  d1_common.util.log_setup(args.debug)

  cn_client = d1_client.cnclient_2_0.CoordinatingNodeClient_2_0(
    base_url=d1_common.const.URL_DATAONE_ROOT
  )

  sysmeta_pyxb = gen_sysmeta.generate_from_file_path(
    cn_client,
    args.path,
    {
      'identifier': 'test_pid',
      'formatId': 'http://www.isotc211.org/2005/gmd',
      'accessPolicy': None,
      'replicationPolicy': None,
      'obsoletes': None,
      'obsoletedBy': None,
      'archived': None,
      'replica': None,
      'mediaType': None,
    },
  )

  with open(args.path, 'rb') as f:
    sciobj_str = f.read()

  response = cn_client.echoIndexedObject(
    'solr', sysmeta_pyxb, StringIO.StringIO(sciobj_str)
  )

  print(d1_common.xml.pretty_xml(response.content))


if __name__ == '__main__':
  main()
