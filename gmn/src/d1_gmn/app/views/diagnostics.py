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
"""Views for GMN diagnostic APIs

These are used in various diagnostics, debugging and testing scenarios. Access
is unrestricted in debug mode. Disabled in production.
"""

from __future__ import absolute_import

# import cgi
# import csv
# import json
# import pprint
#
# import d1_gmn.app.auth
# import d1_gmn.app.db_filter
# import d1_gmn.app.event_log
# import d1_gmn.app.models
# import d1_gmn.app.node_registry
# import d1_gmn.app.psycopg_adapter
# import d1_gmn.app.restrict_to_verb
# import d1_gmn.app.sysmeta
# import d1_gmn.app.util
# import d1_gmn.app.views.asserts
# import d1_gmn.app.views.create
# import d1_gmn.app.views.util
#
# import d1_common.const
# import d1_common.date_time
# import d1_common.types.dataoneTypes
# import d1_common.types.exceptions
#
# import django.apps
# import django.conf
# from django.db.models import Q
# from django.http import HttpResponse
# from django.shortcuts import redirect
# from django.shortcuts import render_to_response

# ------------------------------------------------------------------------------
# Diagnostics portal.
# ------------------------------------------------------------------------------

#
# @d1_gmn.app.restrict_to_verb.get
# def diagnostics(request):
#   return render_to_response(
#     'diag.html', content_type=d1_common.const.CONTENT_TYPE_XHTML
#   )
#
#
# # ------------------------------------------------------------------------------
# # Replication.
# # ------------------------------------------------------------------------------
#
#
# @d1_gmn.app.restrict_to_verb.get
# def get_replication_queue(request):
#   q = d1_gmn.app.models.ReplicationQueue.objects.order_by(
#     'local_replica__info__timestamp', 'local_replica__pid__did'
#   )
#   if 'excludecompleted' in request.GET:
#     q = d1_gmn.app.models.ReplicationQueue.objects.filter(
#       ~Q(local_replica__info__status__status='completed')
#     ).order_by('local_replica__info__timestamp', 'local_replica__pid__did')
#   return render_to_response(
#     'replicate_get_queue.xml', {'replication_queue': q},
#     content_type=d1_common.const.CONTENT_TYPE_XML
#   )
#
#
# # noinspection PyUnusedLocal
# @d1_gmn.app.restrict_to_verb.get
# def clear_replication_queue(request):
#   for rep_queue_model in d1_gmn.app.models.ReplicationQueue.objects.all(
#       #filter(
#       #  local_replica__info__status__status='queued'
#   ).order_by('local_replica__info__timestamp', 'local_replica__pid__did'):
#     d1_gmn.app.models.IdNamespace.objects.filter(
#       did=rep_queue_model.local_replica.pid.did
#     ).delete()
#   return redirect('diag')
#

# ------------------------------------------------------------------------------
# Authentication.
# ------------------------------------------------------------------------------

#
#
# # noinspection PyUnusedLocal
# @d1_gmn.app.restrict_to_verb.get
# def trusted_subjects(request):
#   return render_to_response(
#     'trusted_subjects.xhtml', {
#       'subjects':
#         sorted(
#           d1_gmn.app.node_registry.get_cn_subjects() |
#           django.conf.settings.DATAONE_TRUSTED_SUBJECTS
#         )
#     }, content_type=d1_common.const.CONTENT_TYPE_XHTML
#   )
#
#
# @d1_gmn.app.restrict_to_verb.post
# def whitelist_subject(request):
#   """Add a subject to the whitelist"""
#   subject_model = d1_gmn.app.models.subject(request.POST['subject'])
#   whitelist_model = d1_gmn.app.models.WhitelistForCreateUpdateDelete()
#   whitelist_model.subject = subject_model
#   whitelist_model.save()
#   return d1_gmn.app.views.util.http_response_with_boolean_true_type()

# ------------------------------------------------------------------------------
# Misc.
# ------------------------------------------------------------------------------

# def create(request, pid):
#   """Minimal version of create() used for inserting test objects."""
#   sysmeta_pyxb = d1_gmn.app.views.util.deserialize(request.FILES['sysmeta'])
#   d1_gmn.app.views.create.create(request, sysmeta_pyxb)
#   return d1_gmn.app.views.util.http_response_with_boolean_true_type()
#
#
# # noinspection PyUnusedLocal
# @d1_gmn.app.restrict_to_verb.get
# def slash(request, p1, p2, p3):
#   """Correctly handles arguments separated by slashes"""
#   return render_to_response('test_slash.html', {'p1': p1, 'p2': p2, 'p3': p3})
#

# # noinspection PyUnusedLocal

# @d1_gmn.app.restrict_to_verb.get
# def object_permissions(request, pid):
#   d1_gmn.app.views.asserts.is_existing_object(pid)
#   subjects = []
#   permissions = d1_gmn.app.models.Permission.objects.filter(
#     sciobj__pid__did=pid
#   ).order_by('subject__subject', 'level', 'sciobj__pid__did')
#   for permission in permissions:
#     action = d1_gmn.app.auth.LEVEL_ACTION_MAP[permission.level]
#     subjects.append((permission.subject.subject, action))
#   return render_to_response(
#     'object_permissions.xhtml',
#     locals(), content_type=d1_common.const.CONTENT_TYPE_XHTML
#   )

# # noinspection PyUnusedLocal
# @d1_gmn.app.restrict_to_verb.get
# def get_setting(request, setting_str):
#   """Get a value from django.conf.settings.py or settings.py"""
#   setting_obj = getattr(django.conf.settings, setting_str, '<UNKNOWN SETTING>')
#   if isinstance(setting_obj, set):
#     setting_obj = sorted(list(setting_obj))
#   setting_json = json.dumps(setting_obj)
#   return HttpResponse(setting_json, d1_common.const.CONTENT_TYPE_JSON)

# ------------------------------------------------------------------------------
# Event Log.
# ------------------------------------------------------------------------------

# # noinspection PyUnusedLocal
# def delete_event_log(request):
#   d1_gmn.app.models.Event.objects.all().delete()
#   d1_gmn.app.models.IpAddress.objects.all().delete()
#   d1_gmn.app.models.UserAgent.objects.all().delete()
#   d1_gmn.app.models.EventLog.objects.all().delete()
#   return d1_gmn.app.views.util.http_response_with_boolean_true_type()
#
#
# @d1_gmn.app.restrict_to_verb.post
# def inject_fictional_event_log(request):
#   d1_gmn.app.views.asserts.post_has_mime_parts(request, (('file', 'csv'),))
#
#   # Create event log entries.
#   csv_reader = csv.reader(request.FILES['csv'])
#
#   for row in csv_reader:
#     pid = row[0]
#     event = row[1]
#     ip_address = row[2]
#     user_agent = row[3]
#     # subject = row[4]
#     timestamp = d1_common.date_time.from_iso8601((row[5]))
#     #member_node = row[6]
#
#     # Create fake request object.
#     request.META = {
#       'HTTP_USER_AGENT': user_agent,
#       'REMOTE_ADDR': ip_address,
#       'SERVER_NAME': 'dataone.org',
#       'SERVER_PORT': '80',
#     }
#
#     # noinspection PyProtectedMember
#     d1_gmn.app.event_log._log(
#       pid, request, event, d1_common.date_time.strip_timezone(timestamp)
#     )
#
#   return d1_gmn.app.views.util.http_response_with_boolean_true_type()
