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
''':mod:`settings`
==================

:Synopsis:
 - User configurable settings for ONEDrive.
:Author: DataONE (Dahl)
'''

# Stdlib.
import d1_common.const
import logging
import os
import sys

# D1.


# Create absolute path from path that is relative to the module from which
# the function is called.
def make_absolute(p):
  return os.path.join(os.path.abspath(os.path.dirname(__file__)), p)

################################################################################
# User configurable settings.
################################################################################

# DataONE maintains several instances of the DataONE infrastructure, called
# environments. The production environment is used by the general public. Other
# environments are used by software developers for testing and debugging of new
# components. This setting controls to which environment ONEDrive connects.

# Round-robin CN endpoints
#DATAONE_ROOT = d1_common.const.URL_DATAONE_ROOT # (recommended, production)
#DATAONE_ROOT = 'https://cn-dev.test.dataone.org/cn'
#DATAONE_ROOT = 'https://cn-stage.test.dataone.org/cn' 
#DATAONE_ROOT = 'https://cn-sandbox.dataone.org/cn'
#DATAONE_ROOT = 'https://cn-stage.dataone.org/cn/'
#DATAONE_ROOT = 'https://cn-stage.test.dataone.org/cn'

# Bypass round-robin and go directly to a specific CN.
DATAONE_ROOT = 'https://cn-dev-unm-1.test.dataone.org/cn'

# Select the mountpoint for ONEDrive. The mountpoint is the folder in the local
# filesystem in which the ONEDrive filesystem appears. The default is to mount
# the drive in a folder named "one", in the same folder as the onedrive.py file.
# If the mountpoint is set to a folder that already contains files and folders,
# those files and folders become temporarily invisible while ONEDrive is
# running.
MOUNTPOINT = make_absolute('one') # (default, relative path)
#MOUNTPOINT = '/mnt/onedrive' # (example, absolute path)

# The maximum number of science objects to display in a folder. This setting is
# in effect when there are more science objects available than can be retrieved
# and displayed when a folder is opened. To reach objects that are filtered by
# this setting, use a faceted search to reduce the number of matching objects.
# Increasing this setting causes longer lists of science objects to to appear in
# the filesystem, increases memory footprint for the application and causes
# longer response times when opening folders. Default value: 1000.
MAX_OBJECTS_IN_DIRECTORY = 3

# The maximum number of path attributes to cache. Increasing this number may
# give better performance, but also a larger memory footprint. A value below 100
# is not recommended. Default value: 1000.
MAX_ATTRIBUTE_CACHE_SIZE = 1000

# The maximum number of folders to cache. Increasing this number may give better
# performance, but also a larger memory footprint. A value below 10 is not
# recommended. Default value: 100.
MAX_DIRECTORY_CACHE_SIZE = 100

# The maximum number of science objects to cache. Increasing this number may
# give better performance, but also a larger memory footprint. Default value:
# 10.
MAX_OBJECT_CACHE_SIZE = 10

# The maximum number of error message file paths to cache. Decreasing this
# number below the default is not recommended, as it may cause error messages
# not to be displayed correctly in the ONEDrive filesystem. Default value: 1000.
MAX_ERROR_PATH_CACHE_SIZE = 1000

# The maximum number of faceting selections that can be displayed for a facet.
# The faceting selections are displayed when opening a facet to add a
# restriction to a faceted search. The selections are ordered by the number of
# matching science objects. If there are more faceting selections than this
# setting allows, the selections that match the fewest objects are not
# displayed. Increasing this setting causes longer lists of faceting selections
# to appear in the filesystem, increases memory footprint for the application
# and causes longer response times when opening folders. Default value: 100.
MAX_FACET_VALUES = 100

# The maximum number of facet names for which to cache available facet values.
# Increasing the size of this cache from its default is not necessary, as the
# default value has been chosen to make it unlikely that the cache will
# overflow. Decreasing the size is not recommended, as the cache has very little
# impact on the memory footprint, while holding values which would be expensive
# to keep pulling from DataONE. Default value: 1000.
#MAX_FACET_NAME_CACHE_SIZE = 1000
# TODO: Will probably end up removing this one, as the counts of matching
# objects must be retrieved from SolR, and the values that this cache was
# intended to hold are included with that information.

# The maximum number of SolR query results to cache.
MAX_SOLR_QUERY_CACHE_SIZE = 1000

################################################################################
# Preconfigured searches
################################################################################

# Expert users can use this feature to set up searches that then can be further
# refined through faceted searching in the filesystem. These searches are
# reached through the PreconfiguredSearch root folder in the ONEDrive
# filesystem.

PRECONFIGURED_SEARCHES = {
  'CSV files': [('fq', 'formatId:text/csv')],
  'Objects from Member Node: Demo 5': [('fq', 'datasource:urn\\:node\\:mnDemo5')],
  'PISCO project': [('fq', 'project:Partnership for Interdisciplinary Studies of Coastal Oceans \\\\(PISCO\\\\)')],
}

################################################################################
# Settings below this line are not intended to be modified by the user.
################################################################################

# Debug mode.
# True: Turn on verbose logging and various other debugging facilities.
# False: Log only error messages (for normal use, default)
DEBUG = True

# The facet name and value decorates select the characters which denote
# facet names and facet values in filesystem paths where a faceted search
# is supported.
FACET_NAME_DECORATOR = '@' # (default is '@')
FACET_VALUE_DECORATOR = '#' # (default is '#')

# A list of regular expressions that filter the values returned by the DataONE
# CNRead.getQueryEngineDescription() API to determine which ones are suitable
# for faceting. For a field to be available for faceting, it must be listed as
# searchable in the query engine description and it must NOT match any of the
# the regular expressions in this list.
#FACET_FILTER = [r'.*Text$', r'.*Date$', r'date.*']
FACET_FILTER = [r'.*keywords$', ]

# Type of connection to use when connecting to the Solr server.
# True: A persistent connection is maintained (default)
# False: A new connection is created each time a query is sent
#SOLR_PERSIST_CONNECTION = True

# Objects that match this query are filtered out of all search results.
# None: No filter (default)
SOLR_FILTER_QUERY = None

# The path that is appended to the DataONE root URL to reach the endpoint for
# the DataONE CNRead.query() API.
SOLR_QUERY_PATH = '/v1/query/solr/'

# SOLR_DEBUG_LEVEL:
# Setting this value to 1 causes the Solr client to output debug information.
# True: Turn on debug output in the Solr Client (for debugging)
# False: Turn off debug output (for normal use)
SOLR_DEBUG = True if DEBUG else False # (enabled when running in debug mode)

# FOREGROUND:
# During normal use, the FUSE driver will go into the background, causing the
# onedrive.py command to return immediately. Setting this value to True
# causes the driver to remain in the foreground.
# True: Run driver in foreground (for debugging)
# False: Run driver in background (for normal use) 
#FOREGROUND = True if DEBUG else False # (enabled when running in debug mode)
FOREGROUND = True

# NOTHREADS:
# During normal use, the FUSE drive will use multiple threads to improve
# performance. Settings this value to True causes the driver to run everything
# in a single thread.
# True: Do not create multiple threads (for debugging)
# False: Create multiple threads (for normal use)
NOTHREADS = True if DEBUG else False # (enabled when running in debug mode)

# LOG_LEVEL:
# Set how serious a log message or error must be before it is logged.
# Choices are: DEBUG, INFO, WARNING, ERROR, CRITICAL and NOTSET.
LOG_LEVEL = 'DEBUG' if DEBUG else 'WARNING' # (set according to debug mode)

# Path to the file containing the icon that is displayed for ONEDrive when
# accessing the filesystem through a GUI.
ICON = make_absolute(os.path.join('impl', 'd1.icon'))

# TODO: Describe these.

PATHELEMENT_SAFE_CHARS = ' @$,~*&'
ITERATOR_PER_FETCH = 400
FACET_REFRESH = 20 #seconds between cache refresh for facet values
IGNORE_SPECIAL = []
if os.uname()[0] == "Darwin":
  IGNORE_SPECIAL = ['._', '.DS_Store', 'Backups.backupdb', '.Trashes', ]
TSTAMP = 1280664000.0 #2010-08-01T08:00:00
