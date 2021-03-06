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
"""General utilities often needed by DataONE clients and servers.
"""

from __future__ import absolute_import

import contextlib
import email.message
import email.utils
import errno
import functools
import json
import logging
import os
import sys


def log_setup(is_debug=False, is_multiprocess=False):
  """Set up a standardized log format for the DataONE Python stack. All Python
  components should use this function. If {is_multiprocess} is True, include
  process ID in the log so that logs can be separated for each process.

  Output only to stdout and stderr.
  """
  format_str = (
    u'%(asctime)s %(name)s %(module)s %(process)4d %(levelname)-8s %(message)s'
    if is_multiprocess else
    u'%(asctime)s %(name)s %(module)s %(levelname)-8s %(message)s'
  )
  formatter = logging.Formatter(format_str, u'%Y-%m-%d %H:%M:%S')
  console_logger = logging.StreamHandler(sys.stdout)
  console_logger.setFormatter(formatter)
  logging.getLogger('').addHandler(console_logger)
  if is_debug:
    logging.getLogger('').setLevel(logging.DEBUG)
  else:
    logging.getLogger('').setLevel(logging.INFO)


def abs_path(rel_path):
  """Convert a path that is relative to the module from which this function is
  called, to an absolute path.
  """
  return os.path.abspath(
    os.path.
    join(os.path.dirname(sys._getframe(1).f_code.co_filename), rel_path)
  )


def abs_path_from_base(base_path, rel_path):
  """Join {rel_path} to {base_path} and return an absolute path to the resulting
  location
  """
  return os.path.abspath(
    os.path.join(
      os.path.dirname(sys._getframe(1).f_code.co_filename), base_path, rel_path
    )
  )


def create_missing_directories_for_dir(dir_path):
  try:
    os.makedirs(dir_path)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise


def create_missing_directories_for_file(file_path):
  create_missing_directories_for_dir(os.path.dirname(file_path))


def get_content_type(content_type):
  m = email.message.Message()
  m['Content-Type'] = content_type
  return m.get_content_type()


def utf8_to_unicode(f):
  """Decorator that converts string arguments to Unicode. Assumes that strings
  contains ASCII or utf-8. All other argument types are passed through
  untouched.

  A UnicodeDecodeError raised here means that the wrapped function was called
  with a string argument that did not contain ASCII or utf-8. In such a case,
  the user is required to convert the string to Unicode before passing it to the
  function.
  """

  @functools.wraps(f)
  def wrapper(*args, **kwargs):
    new_args = []
    new_kwargs = {}
    for arg in args:
      if type(arg) is str:
        # See function docstring if UnicodeDecodeError is raised here.
        new_args.append(arg.decode('utf-8'))
      else:
        new_args.append(arg)
    for key, arg in kwargs.items():
      if type(arg) is str:
        # See function docstring if UnicodeDecodeError is raised here.
        new_kwargs[key] = arg.decode('utf-8')
      else:
        new_kwargs[key] = arg
    return f(*new_args, **new_kwargs)

  return wrapper


def unicode_to_utf8(f):
  @functools.wraps(f)
  def wrapper(*args, **kwargs):
    return f(
      *[v.encode('utf-8') if isinstance(v, unicode) else v for v in args], **{
        k: v.encode('utf-8') if isinstance(v, unicode) else v
        for k, v in kwargs.items()
      }
    )

  return wrapper


#===============================================================================


class EventCounter(object):
  def __init__(self):
    self._event_dict = {}

  @property
  def event_dict(self):
    return self._event_dict

  def count(self, event_str, inc_int=1):
    self._event_dict.setdefault(event_str, 0)
    self._event_dict[event_str] += inc_int

  def log_and_count(self, event_str, msg_str=None, inc_int=None):
    """{event_str} is both a key for the count and part of the log message.
    {log_str} is a message with details that may change for each call
    """
    logging.info(
      u' - '.join([v for v in (event_str, msg_str, str(inc_int)) if v])
    )
    self.count(event_str, inc_int or 1)

  def dump_to_log(self):
    if self._event_dict:
      logging.info('Events:')
      for event_str, count_int in sorted(self._event_dict.items()):
        logging.info('  {}: {}'.format(event_str, count_int))
    else:
      logging.info('No Events')


#===============================================================================


@contextlib.contextmanager
def print_logging():
  """Temporarily remove all formatting from logging.

  Creates a logger that writes only the logged strings. This makes logging look
  like print(). The main use case is in scripts that mix logging and print(), as
  Python uses separate streams for those, and output can, and does, end up
  getting shuffled up. Also, it can be used as a "print with log level".

  This works by saving the logging levels on the current handlers, setting
  them to something high, so they don't interfere unless it's something
  serious. Then, adding a handler without formatting with debug level logging.
  When leaving the context, remove the old handler and restore the log levels.
  """
  root_logger = logging.getLogger()
  old_level_list = [h.level for h in root_logger.handlers]
  for h in root_logger.handlers:
    h.setLevel(logging.WARN)
  log_format = logging.Formatter('%(message)s')
  stream_handler = logging.StreamHandler(sys.stdout)
  stream_handler.setFormatter(log_format)
  stream_handler.setLevel(logging.DEBUG)
  root_logger.addHandler(stream_handler)
  yield
  root_logger.removeHandler(stream_handler)
  for h, level in zip(root_logger.handlers, old_level_list):
    h.setLevel(level)


def save_json(py_obj, json_path):
  with open(json_path, 'w') as f:
    f.write(format_normalized_pretty_json(py_obj))


def load_json(json_path):
  with open(json_path, 'r') as f:
    return json.load(f)


def format_normalized_pretty_json(py_obj):
  return json.dumps(py_obj, sort_keys=True, indent=2, cls=SetToList)


def format_normalized_compact_json(py_obj):
  return json.dumps(
    py_obj, sort_keys=True, separators=(',', ':'), cls=SetToList
  )


class SetToList(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, set):
      return sorted(list(obj))
    return json.JSONEncoder.default(self, obj)
