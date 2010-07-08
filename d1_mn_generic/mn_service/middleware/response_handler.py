#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
:mod:`response_handler`
=========================

:platform: Linux
:Synopsis:
  Serialize DataONE response objects according to Accept header and set header
  (Size and Content-Type) accordingly.

.. moduleauthor:: Roger Dahl
'''

# Stdlib.
import csv
import datetime
import os
import StringIO
import sys
import types
import urllib
import wsgiref.handlers
import time

try:
  import cjson as json
except:
  import json

# 3rd party.
# Lxml
try:
  from lxml import etree
except ImportError, e:
  sys.stderr.write('Import error: {0}\n'.format(str(e)))
  sys.stderr.write('Try: sudo apt-get install python-lxml\n')
  raise

import d1common.ext.mimeparser

# Django.
#from django.utils.html import escape
#from django.conf import settings
#from django.shortcuts import render_to_response
#from django.template import Context
#from django.template import RequestContext
from django.db import models

from django.http import HttpResponse

# MN API.
import d1common.exceptions
import d1common.types.objectlist_serialization

# App.
import mn_service.models as models
import mn_service.sys_log as sys_log
import mn_service.util as util
import settings


class ObjectList(d1common.types.objectlist_serialization.ObjectList):
  def deserializeDB(self, view_result):
    '''
    '''
    objectInfos = []

    for row in view_result['query']:
      print row
      objectInfo = d1common.types.generated.objectlist.ObjectInfo()

      objectInfo.identifier = row.guid
      objectInfo.objectFormat = row.format.format
      objectInfo.checksum = row.checksum
      objectInfo.checksum.algorithm = row.checksum_algorithm.checksum_algorithm
      objectInfo.dateSysMetadataModified = datetime.datetime.isoformat(row.mtime)
      objectInfo.size = row.size

      objectInfos.append(objectInfo)

    self.object_list.start = view_result['start']
    self.object_list.count = len(objectInfos)
    self.object_list.total = view_result['total']

    self.object_list.objectInfo = objectInfos


def serialize_object(request, view_result):
  # The "pretty" parameter generates pretty response.
  pretty = 'pretty' in request.REQUEST

  # For JSON, we support giving a variable name.
  if 'jsonvar' in request.REQUEST:
    jsonvar = request.REQUEST['jsonvar']
  else:
    jsonvar = False

  # Serialize to response in requested format.
  response = HttpResponse()
  object_list = ObjectList()
  object_list.deserializeDB(view_result)

  if 'HTTP_ACCEPT' in request.META:
    accept = request.META['HTTP_ACCEPT']
  else:
    accept = None

  doc, content_type = object_list.serialize(accept, pretty, jsonvar)
  response.write(doc)

  # Set headers.
  set_header(response, None, response.tell(), content_type)

  return response

# Monitoring.

#else:
#  for row in query:
#    monitor.append(((str(row['day']), str(row['count']))))
#  monitor.append(('null', query.aggregate(count=Count('id'))['count']))
#
#response.monitor = monitor
#return response


#{
#  [
#    {
#      'guid':<identifier>,
#      'oclass':<object class>,
#      'checksum': {'algorithm': _algorithm used for checksum_, 'value': _checksum of object_}
#      'modified':<date time last modified>,
#      'size':<byte size of object>
#    },
#    ...
#  ]
#}
def monitor_serialize_json(monitor, jsonvar=False):
  '''
  Serialize object to JSON.
  '''

  if jsonvar is not False:
    return jsonvar + '=' + json.dumps(monitor)
  else:
    return json.dumps(monitor)


#<response xmlns='http://ns.dataone.org/core/objects'
#  <data guid='_identifier_'>
#    <oclass>_object class_</oclass>
#    <checksum>
#     <algorithm>_algorithm used for checksum_</algorithm>
#     <value>_checksum of object_</value>
#    </checksum>
#    <modified>_date time last modified_</modified>
#    <size>_byte size of object_</size>
#  </data>
#  ...
#</response>
def monitor_serialize_xml(monitor, jsonvar=False):
  '''
  Serialize object to XML.
  '''

  # Set up namespace for the xml response.
  RESPONSE_NS = 'http://ns.dataone.org/core/objects'
  RESPONSE = '{{{0}}}'.format(RESPONSE_NS)
  NSMAP = {'d1': RESPONSE_NS} # the default namespace
  xml = etree.Element(RESPONSE + 'monitor', nsmap=NSMAP)

  #if 'objectInfo' in obj:
  #  for d in obj['objectInfo']:
  #    data = etree.SubElement(xml, 'objectInfo')
  #    
  #    for key in sorted(d.keys()):
  #      ele = etree.SubElement(data, unicode(key))
  #      ele.text = unicode(d[key])

  for row in monitor:
    data = etree.SubElement(xml, 'day')
    ele = etree.SubElement(data, 'date')
    ele.text = unicode(row[0])
    ele = etree.SubElement(data, 'count')
    ele.text = unicode(row[1])

    # Return xml as string.
  io = StringIO.StringIO()
  io.write(etree.tostring(xml, encoding='UTF-8', xml_declaration=True))
  return io.getvalue()


def monitor_serialize_null(monitor, jsonvar=False):
  '''
  For now, this NULL serializer just calls out to the json serializer.
  '''
  return monitor_serialize_json(monitor, jsonvar)


def monitor_serialize_object(request, response, monitor):
  map = {
    'application/json': monitor_serialize_json,
    'text/csv': monitor_serialize_null,
    'text/xml': monitor_serialize_xml,
    #'application/rdf+xml': monitor_serialize_null,
    'text/html': monitor_serialize_null,
    'text/log': monitor_serialize_null,
  }

  pri = [
    'application/json',
    'text/csv',
    'text/xml',
    #'application/rdf+xml',
    'text/html',
    'text/log',
  ]

  # For JSON, we support giving a variable name.
  if 'jsonvar' in request.GET:
    jsonvar = request.GET['jsonvar']
  else:
    jsonvar = False

  # Determine which serializer to use. If client does not supply HTTP_ACCEPT,
  # we default to JSON.
  content_type = 'application/json'
  if 'HTTP_ACCEPT' not in request.META:
    sys_log.debug('No HTTP_ACCEPT header. Defaulting to JSON')
  else:
    try:
      content_type = d1common.ext.mimeparser.best_match(pri, request.META['HTTP_ACCEPT'])
    except ValueError:
      # An invalid Accept header causes mimeparser to throw a ValueError. In
      # that case, we also default to JSON.
      sys_log.debug('Invalid HTTP_ACCEPT header. Defaulting to JSON')

  # Serialize object.
  obj_ser = map[content_type](monitor, jsonvar)

  # Add the serialized object to the response.
  response.write(obj_ser)

  # Set headers.
  set_header(response, None, len(obj_ser), content_type)

  return response


def set_header(response, last_modified, content_length, content_type):
  '''
  Add Last-Modified, Content-Length and Content-Type headers to response.

  If last_modified is None, we pull the date from the one stored in the db.
  '''
  if last_modified is None:
    try:
      status_row = models.DB_update_status.objects.all()[0]
    except IndexError:
      last_modified = datetime.datetime.now()
    else:
      last_modified = status_row.mtime

  response['Last-Modified'] = wsgiref.handlers.format_date_time(
    time.mktime(
      last_modified.timetuple(
      )
    )
  )
  response['Content-Length'] = content_length
  response['Content-Type'] = content_type


class response_handler():
  def process_response(self, request, view_result):
    # If response is a query, we run the query and create a response.
    if type(view_result) == dict:
      #if isinstance(response, models.models.query.QuerySet):
      response = serialize_object(request, view_result)
    # If view_result is a HttpResponse, we return it unprocessed.
    else:
      response = view_result

    # For debugging, if pretty printed outout was requested, we force the
    # content type to text.
    if 'pretty' in request.REQUEST:
      response['Content-Type'] = 'text/plain'

    # If view_result is a HttpResponse, we return it unprocessed.
    return response
