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
"""MNPackage.getPackage(session, packageType, id) → OctetStream"""
import d1_gmn.app.resource_map
import d1_gmn.app.restrict_to_verb
import d1_gmn.app.sciobj_store
import d1_gmn.app.util
import d1_gmn.app.views.decorators

import d1_common.bagit
import d1_common.const
import d1_common.iter.file
import d1_common.types.exceptions

import django.http


def get_package(request, pid, package_type):
  # Convert args from keyword to positional
  return _get_package(request, pid, package_type)


@d1_gmn.app.restrict_to_verb.get
@d1_gmn.app.views.decorators.decode_id
@d1_gmn.app.views.decorators.resolve_sid
@d1_gmn.app.views.decorators.read_permission
def _get_package(request, pid, package_type):
  if package_type != d1_common.const.DEFAULT_DATA_PACKAGE_FORMAT_ID:
    raise d1_common.types.exceptions.InvalidRequest(
      0, u'Unsupported Data Package format. '
      u'Currently, only BagIt (formatId={}) is supported'.
      format(d1_common.const.DEFAULT_DATA_PACKAGE_FORMAT_ID)
    )
  pid_list = d1_gmn.app.resource_map.get_resource_map_members(pid)
  sciobj_info_list = _create_sciobj_info_list(pid_list)
  bagit_file = d1_common.bagit.create_bagit_stream(pid, sciobj_info_list)
  response = django.http.StreamingHttpResponse(
    bagit_file, content_type='application/zip'
  )
  response['Content-Disposition'
           ] = 'attachment; filename={}'.format('files.zip')
  return response


def _create_sciobj_info_list(pid_list):
  sciobj_info_list = []
  for pid in pid_list:
    if not d1_gmn.app.sciobj_store.is_existing_sciobj_file(pid):
      continue
    sciobj_info_list.append(_create_sciobj_info_dict(pid))
  return sciobj_info_list


def _create_sciobj_info_dict(pid):
  sciobj_model = d1_gmn.app.util.get_sci_model(pid)
  return {
    'pid': pid,
    'filename': sciobj_model.filename,
    'iter': _create_sciobj_iterator(pid),
    'checksum': sciobj_model.checksum,
    'checksum_algorithm': sciobj_model.checksum_algorithm.checksum_algorithm
  }


def _create_sciobj_iterator(pid):
  return d1_common.iter.file.FileIterator(
    d1_gmn.app.sciobj_store.get_sciobj_file_path(pid)
  )