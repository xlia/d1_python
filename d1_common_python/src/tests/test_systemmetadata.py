#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright ${year}
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
'''
Module d1_common.tests.test_systemmetadata
==========================================

Unit tests for serializaton and de-serialization of the SystemMetadata type.

:Created: 2010-06-29
:Author: DataONE (vieglais, dahl)
:Dependencies:
  - python 2.6
'''

import logging
import sys
import unittest

import pyxb
from d1_common import xmlrunner
import d1_common.types.exceptions
from d1_common.types import systemmetadata

EG_SYSMETA = u"""<?xml version="1.0" encoding="UTF-8"?>
<d1:systemMetadata xmlns:d1="http://dataone.org/service/types/0.5.1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://dataone.org/service/types/0.5.1 https://repository.dataone.org/software/cicore/tags/D1_SCHEMA_0_5_1/dataoneTypes.xsd">
    <!-- This instance document was auto generated by oXygen XML for testing purposes.
         It contains no useful information.
    -->
    <identifier>Identifier0</identifier>
    <objectFormat>eml://ecoinformatics.org/eml-2.0.1</objectFormat>
    <size>0</size>
    <submitter>uid=jones,o=NCEAS,dc=ecoinformatics,dc=org</submitter>
    <rightsHolder>uid=jones,o=NCEAS,dc=ecoinformatics,dc=org</rightsHolder>
    <obsoletes>Obsoletes0</obsoletes>
    <obsoletes>Obsoletes1</obsoletes>
    <obsoletedBy>ObsoletedBy0</obsoletedBy>
    <obsoletedBy>ObsoletedBy1</obsoletedBy>
    <derivedFrom>DerivedFrom0</derivedFrom>
    <derivedFrom>DerivedFrom1</derivedFrom>
    <describes>Describes0</describes>
    <describes>Describes1</describes>
    <describedBy>DescribedBy0</describedBy>
    <describedBy>DescribedBy1</describedBy>
    <checksum algorithm="SHA-1">2e01e17467891f7c933dbaa00e1459d23db3fe4f</checksum>
    <embargoExpires>2006-05-04T18:13:51.0Z</embargoExpires>
    <accessRule rule="allow" service="read" principal="Principal0"/>
    <accessRule rule="allow" service="read" principal="Principal1"/>
    <replicationPolicy replicationAllowed="true" numberReplicas="2">
        <preferredMemberNode>MemberNode12</preferredMemberNode>
        <preferredMemberNode>MemberNode13</preferredMemberNode>
        <blockedMemberNode>MemberNode6</blockedMemberNode>
        <blockedMemberNode>MemberNode7</blockedMemberNode>
    </replicationPolicy>
    <dateUploaded>2006-05-04T18:13:51.0Z</dateUploaded>
    <dateSysMetadataModified>2006-05-04T18:13:51.0Z</dateSysMetadataModified>
    <originMemberNode>OriginMemberNode0</originMemberNode>
    <authoritativeMemberNode>AuthoritativeMemberNode0</authoritativeMemberNode>
    <replica>
        <replicaMemberNode>ReplicaMemberNode0</replicaMemberNode>
        <replicationStatus>queued</replicationStatus>
        <replicaVerified>2006-05-04T18:13:51.0Z</replicaVerified>
    </replica>
    <replica>
        <replicaMemberNode>ReplicaMemberNode1</replicaMemberNode>
        <replicationStatus>queued</replicationStatus>
        <replicaVerified>2006-05-04T18:13:51.0Z</replicaVerified>
    </replica>
</d1:systemMetadata>
"""

EG_BAD_SYSMETA = u"""<?xml version="1.0" encoding="UTF-8"?>
<d1:systemMetadata xmlns:d1="http://dataone.org/service/types/0.5.1"
 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
 xsi:schemaLocation="http://dataone.org/service/types/0.5.1 https://repository.dataone.org/software/cicore/tags/D1_SCHEMA_0_5_1/dataoneTypes.xsd">
    <!-- This instance document was auto generated by oXygen XML for testing purposes.
         It contains no useful information.
    -->
    <!-- <identifier>Identifier0</identifier> -->
    <objectFormat>eml://ecoinformatics.org/eml-2.0.1</objectFormat>
    <size>0</size>
    <submitter>uid=jones,o=NCEAS,dc=ecoinformatics,dc=org</submitter>
    <rightsHolder>uid=jones,o=NCEAS,dc=ecoinformatics,dc=org</rightsHolder>
    <obsoletes>Obsoletes0</obsoletes>
    <obsoletes>Obsoletes1</obsoletes>
    <obsoletedBy>ObsoletedBy0</obsoletedBy>
    <obsoletedBy>ObsoletedBy1</obsoletedBy>
    <derivedFrom>DerivedFrom0</derivedFrom>
    <derivedFrom>DerivedFrom1</derivedFrom>
    <describes>Describes0</describes>
    <describes>Describes1</describes>
    <describedBy>DescribedBy0</describedBy>
    <describedBy>DescribedBy1</describedBy>
    <checksum algorithm="SHA-1">2e01e17467891f7c933dbaa00e1459d23db3fe4f</checksum>
    <embargoExpires>2006-05-04T18:13:51.0Z</embargoExpires>
    <accessRule rule="allow" service="read"/>
    <accessRule rule="allow" service="read" principal="Principal1"/>
    <replicationPolicy replicationAllowed="true" numberReplicas="2">
        <preferredMemberNode>MemberNode12</preferredMemberNode>
        <preferredMemberNode>MemberNode13</preferredMemberNode>
        <blockedMemberNode>MemberNode6</blockedMemberNode>
        <blockedMemberNode>MemberNode7</blockedMemberNode>
    </replicationPolicy>
    <dateUploaded>2006-05-04T18:13:51.0Z</dateUploaded>
    <dateSysMetadataModified>2006-05-04T18:13:51.0Z</dateSysMetadataModified>
    <originMemberNode>OriginMemberNode0</originMemberNode>
    <authoritativeMemberNode>AuthoritativeMemberNode0</authoritativeMemberNode>
    <replica>
        <replicaMemberNode>ReplicaMemberNode0</replicaMemberNode>
        <replicationStatus>queued</replicationStatus>
        <replicaVerified>2006-05-04T18:13:51.0Z</replicaVerified>
    </replica>
    <replica>
        <replicaMemberNode>ReplicaMemberNode1</replicaMemberNode>
        <replicationStatus>queued</replicationStatus>
        <replicaVerified>2006-05-04T18:13:51.0Z</replicaVerified>
    </replica>
</d1:systemMetadata>
"""


class TestSystemMetadata(unittest.TestCase):
  def testLoadSystemMetadata(self):
    sysm = systemmetadata.CreateFromDocument(EG_SYSMETA)
    self.assertEqual(sysm.identifier.value(), 'Identifier0')
    self.assertEqual(sysm.size, 0)
    self.assertEqual(sysm.checksum.algorithm, 'SHA-1')
    self.assertEqual(sysm.checksum.value(), '2e01e17467891f7c933dbaa00e1459d23db3fe4f')
    rep = sysm.replica
    self.assertEqual(len(rep), 2)
    self.assertEqual(rep[1].replicationStatus, 'queued')
    try:
      bogus = sysm.thisDoesntExist
    except Exception, e:
      pass
    self.assertTrue(isinstance(e, AttributeError))
    #should fail with NotImplemented
    self.assertRaises(d1_common.types.exceptions.NotImplemented, sysm.toJSON)
    self.assertRaises(d1_common.types.exceptions.NotImplemented, sysm.toCSV)

  def testValidateSystemMetadata(self):
    #Try loading a bad document with validation turned on.
    #Should fail with an "UnrecognizedContentError"
    try:
      sysm = systemmetadata.CreateFromDocument(EG_BAD_SYSMETA)
      self.assertFalse(sysm)
    except Exception, e:
      logging.debug(repr(e))
      self.assertTrue(isinstance(e, pyxb.UnrecognizedContentError))
    #Turning off validation should not raise an exception
    pyxb.RequireValidWhenParsing(False)
    try:
      sysm = systemmetadata.CreateFromDocument(EG_BAD_SYSMETA)
      self.assertTrue(True)
    except Exception, e:
      logging.debug(repr(e))
      self.assertFalse(isinstance(e, pyxb.UnrecognizedContentError))
    #Turn validation back on and check for error
    pyxb.RequireValidWhenParsing(True)
    sysm = systemmetadata.CreateFromDocument(EG_SYSMETA)

#===============================================================================
if __name__ == "__main__":
  argv = sys.argv
  if "--debug" in argv:
    logging.basicConfig(level=logging.DEBUG)
    argv.remove("--debug")
  if "--with-xunit" in argv:
    argv.remove("--with-xunit")
    unittest.main(argv=argv, testRunner=xmlrunner.XmlTestRunner(sys.stdout))
  else:
    unittest.main(argv=argv)
