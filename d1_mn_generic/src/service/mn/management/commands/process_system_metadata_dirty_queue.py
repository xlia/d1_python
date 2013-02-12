#!/usr/bin/env python
# -*- coding: utf-8 -*-

# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2012 DataONE
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
"""
:mod:`process_system_metadata_dirty_queue`
==========================================

:Synopsis: 
  Iterate over queue of objects registered to have their System Metadata
  refreshed and refresh them by pulling the latest version from a CN.
:Created: 2011-11-8
:Author: DataONE (Dahl)
"""

# Stdlib.
import logging
import os
import sys
import urlparse

# Django.
from django.core.exceptions import ImproperlyConfigured
from django.core.management.base import BaseCommand
from django.core.management.base import NoArgsCommand
from django.core.management.base import CommandError
#from django.http import HttpResponse
#from django.http import Http404
#from django.template import Context
#from django.template import loader
#from django.shortcuts import render_to_response
#from django.utils.html import escape
import django.utils.log
import django.db.models

# D1.
import d1_common.const
import d1_common.types.generated.dataoneTypes as dataoneTypes
import d1_common.types.exceptions
import d1_common.util
import d1_common.date_time
import d1_common.url
import d1_client.d1client

# App.
import settings
import mn.models


class Command(NoArgsCommand):
  help = 'Process the System Metadata dirty queue.'

  def handle_noargs(self, **options):
    self.log_setup()

    logging.info('Running management command: ' 'process_system_metadata_dirty_queue')

    verbosity = int(options.get('verbosity', 1))

    if verbosity <= 1:
      logging.getLogger('').setLevel(logging.ERROR)

    self.process_queue()

  def process_queue(self):
    for queue_item in mn.models.SystemMetadataDirtyQueue.objects.filter(
      ~django.db.models.Q(status__status='completed')
    ):
      logging.info('Refreshing System Metadata: {0}'.format(queue_item.object.pid))
      self.process_queue_item(queue_item)

    self.delete_completed_queue_items_from_db()

  def process_queue_item(self, queue_item):
    self.update_queue_item_status(queue_item, 'processing')
    try:
      response = self.get_sysmeta_from_cn_and_post_to_gmn(queue_item)
      if response.status != 200:
        raise Exception('Bad response: {0}'.format(response.status))
    except d1_common.types.exceptions.DataONEException as e:
      logging.error(str(e))
      self.update_queue_item_status(queue_item, 'failed')
    except Exception, e:
      logging.error(str(e))
      self.update_queue_item_status(queue_item, 'failed')
      raise
    else:
      self.update_queue_item_status(queue_item, 'completed')

  def generate_mime_multipart_document_and_post_to_gmn(self, pid, sysmeta):
    sysmeta_xml = sysmeta.toxml()
    files = [('sysmeta', 'sysmeta', sysmeta_xml.encode('utf-8')), ]
    client = d1_client.mnclient.MemberNodeClient(settings.LOCAL_BASE_URL)
    response = client.POST(self.get_internal_update_sysmeta_url(pid), files=files)
    return response

  def get_sysmeta_from_cn_and_post_to_gmn(self, queue_item):
    pid = queue_item.object.pid
    sysmeta = self.get_sysmeta_from_cn(pid)
    response = self.generate_mime_multipart_document_and_post_to_gmn(pid, sysmeta)
    return response

  def get_sysmeta_from_cn(self, pid):
    # d1_common.const.URL_DATAONE_ROOT
    client = d1_client.d1client.DataONEClient(
      settings.LOCAL_BASE_URL
    ) ### settings.LOCAL_BASE_URL is for testing.
    sysmeta = client.getSystemMetadata(pid)
    return sysmeta

  def get_internal_update_sysmeta_url(self, pid):
    return urlparse.urljoin(
      settings.LOCAL_BASE_URL,
      'internal_update_sysmeta/{0}'.format(d1_common.url.encodePathElement(pid))
    )

  def update_queue_item_status(self, queue_item, status):
    queue_item.set_status(status)
    queue_item.save()

  def delete_completed_queue_items_from_db(self):
    mn.models.SystemMetadataDirtyQueue.objects.filter(status__status='completed').delete()

  def log_setup(self):
    # Set up logging. We output only to stdout. Instead of also writing to a log
    # file, redirect stdout to a log file when the script is executed from cron.
    logging.getLogger('').setLevel(logging.DEBUG)
    formatter = logging.Formatter(
      '%(asctime)s %(levelname)-8s %(name)s %(module)s %(message)s', '%Y-%m-%d %H:%M:%S'
    )
    console_logger = logging.StreamHandler(sys.stdout)
    console_logger.setFormatter(formatter)
    logging.getLogger('').addHandler(console_logger)
