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
"""Mock Requests to issue requests through the Django test client

Django includes a test framework with a test client that provides an interface
that's similar to that of an HTTP client, but calls Django internals directly.
The client enables testing of most functionality of a Django app without
actually starting the app as a network service.

For testing GMN's D1 REST interfaces, we want to issue the test requests via the
D1 MN client. Without going through the D1 MN client, we would have to
reimplement much of what the client does, related to formatting and parsing D1
REST requests.

This module is typically used in tests running under django.test.TestCase
and requires an active Django context, such as the one provided by
`./manage.py test`.

Usage:

import d1_test.mock_api.django_client as mock_django_client

@responses.activate
def test_1000(self):
  mock_django_client.add_callback(BASE_URL)
  d1_client = d1_client.mnclient_2_0.MemberNodeClient_2_0(BASE_URL)
  node_pyxb = d1_client.getCapabilities()

Note: for get(), GMN returns a StreamingHttpResponse that Requests detects as a
streaming response and handles accordingly. However, when returning a
StreamingHttpResponse from Responses, no special handling occurs. This breaks
test code that converts streams to strings by accessing .content (production
code should not do this since it causes the entire stream to be buffered in
memory). So we convert streaming responses to string before passing them to
Responses.
"""

import logging
import re

import d1_test.mock_api.d1_exception
import d1_test.mock_api.util
import django.test
import requests_toolbelt
import responses


def add_callback(base_url):
  for method in [
      responses.DELETE, responses.GET, responses.HEAD, responses.OPTIONS,
      responses.PATCH, responses.POST, responses.PUT
  ]:
    responses.add_callback(
      method,
      re.compile('^{}'.format(base_url)),
      callback=_request_callback,
      content_type='',
    )
    logging.debug(
      'Added callback. method="{}" base_url="{}"'.format(method, base_url)
    )


def _request_callback(request):
  method = request.method
  url_path = u'/{}/{}'.format(
    *d1_test.mock_api.util.split_url_at_version_tag(request.url)[1:]
  )
  django_client = django.test.Client()

  if isinstance(request.body, requests_toolbelt.MultipartEncoder):
    data = request.body.read()
  else:
    data = request.body

  django_response = getattr(django_client, method.lower())(
    url_path, data=data, content_type=request.headers.get('Content-Type'),
    **_headers_to_wsgi_env(request.headers or {})
  )

  return (
    django_response.status_code, django_response.items(),
    ''.join(django_response.streaming_content)
    if django_response.streaming else django_response.content,
  )


def _headers_to_wsgi_env(header_dict):
  wsgi_dict = header_dict.copy()
  wsgi_dict.update({
    'HTTP_' + k.upper().replace('-', '_'): v for k, v in header_dict.items()
  })
  return wsgi_dict
