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

from __future__ import absolute_import

import datetime

import responses

import d1_common.types.dataoneTypes as dataoneTypes

import d1_test.d1_test_case
import d1_test.mock_api.get_log_records as mock_get_log_records

import d1_client.cnclient
import d1_client.iter.logrecord_multi
import d1_client.mnclient


class TestLogRecordIterator(d1_test.d1_test_case.D1TestCase):
  @responses.activate
  def test_1000(self):
    """PageSize=5, start=0"""
    mock_get_log_records.add_callback(d1_test.d1_test_case.MOCK_BASE_URL)
    self._log_record_iterator_test(5)

  def _test_110(self):
    """PageSize=1, start=63"""
    self._log_record_iterator_test(1)

  def _test_130(self):
    """PageSize=5, start=10, fromDate=2005-01-01"""
    self._log_record_iterator_test(
      2000, from_date=datetime.datetime(2005, 1, 1)
    )

  def _log_record_iterator_test(self, page_size, from_date=None, to_date=None):
    log_record_iterator = d1_client.iter.logrecord_multi.LogRecordIteratorMulti(
      base_url=d1_test.d1_test_case.MOCK_BASE_URL,
      # base_url='https://gmn2/mn',
      page_size=page_size,
      api_major=2, # api_major = d1_client.util.get_version_tag_by_d1_client(mn_client_v1_v2)
      client_dict={
        'verify_tls': False,
        'timeout_sec': 0,
      },
      get_log_records_dict={
        'fromDate': from_date,
        'toDate': to_date,
      },
    )
    cnt = 0
    for log_entry in log_record_iterator:
      assert isinstance(log_entry, dataoneTypes.LogEntry)
      # logging.info("Event      = {}".format(log_entry.event))
      # logging.info("Timestamp  = {}".format(log_entry.dateLogged.isoformat()))
      # logging.info("IP Address = {}".format(log_entry.ipAddress))
      # logging.info("Identifier = {}".format(log_entry.identifier.value()))
      # logging.info("User agent = {}".format(log_entry.userAgent))
      # logging.info("Subject    = {}".format(log_entry.subject.value()))
      # logging.info('-' * 100)
      cnt += 1
