# This work was created by participants in the DataONE project, and is
# jointly copyrighted by participating institutions in DataONE. For
# more information on DataONE, see our web site at http://dataone.org.
#
#   Copyright 2009-2017 DataONE
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
Constants used by the DataONE drive for Windows which is built using Dokan.
"""

# IO error codes
ERROR_FILE_NOT_FOUND = 2
ERROR_PATH_NOT_FOUND = 3
ERROR_ACCESS_DENIED = 5
ERROR_SHARING_VIOLATION = 32
ERROR_INVALID_NAME = 123
ERROR_FILE_EXISTS = 80
ERROR_ALREADY_EXISTS = 183

# general error codes
DOKAN_SUCCESS = 0
DOKAN_ERROR = -1
DOKAN_DRIVE_LETTER_ERROR = -2
DOKAN_DRIVER_INSTALL_ERROR = -3
DOKAN_START_ERROR = -4
DOKAN_MOUNT_ERROR = -5
DOKAN_MOUNT_POINT_ERROR = -6

# version
DOKAN_VERSION = 600

# mount options
DOKAN_OPTION_DEBUG = 1
DOKAN_OPTION_STDERR = 2
DOKAN_OPTION_ALT_STREAM = 4
DOKAN_OPTION_KEEP_ALIVE = 8
DOKAN_OPTION_NETWORK = 16
DOKAN_OPTION_REMOVABLE = 32

# native Windows flags for volume description
FILE_CASE_SENSITIVE_SEARCH = 0x00000001
FILE_CASE_PRESERVED_NAMES = 0x00000002
FILE_UNICODE_ON_DISK = 0x00000004
FILE_PERSISTENT_ACLS = 0x00000008
FILE_FILE_COMPRESSION = 0x00000010
FILE_VOLUME_QUOTAS = 0x00000020
FILE_SUPPORTS_SPARSE_FILES = 0x00000040
FILE_SUPPORTS_REPARSE_POINTS = 0x00000080
FILE_SUPPORTS_REMOTE_STORAGE = 0x00000100
FS_LFN_APIS = 0x00004000
FILE_VOLUME_IS_COMPRESSED = 0x00008000
FILE_SUPPORTS_OBJECT_IDS = 0x00010000
FILE_SUPPORTS_ENCRYPTION = 0x00020000
FILE_NAMED_STREAMS = 0x00040000
FILE_READ_ONLY_VOLUME = 0x00080000
FILE_SEQUENTIAL_WRITE_ONCE = 0x00100000
FILE_SUPPORTS_EXTENDED_ATTRIBUTES = 0x00800000
FILE_SUPPORTS_HARD_LINKS = 0x00400000
FILE_SUPPORTS_OPEN_BY_FILE_ID = 0x01000000
FILE_SUPPORTS_TRANSACTIONS = 0x00200000
FILE_SUPPORTS_USN_JOURNAL = 0x02000000

# file attribute flags
FILE_ATTRIBUTE_READONLY = 0x00000001
FILE_ATTRIBUTE_HIDDEN = 0x00000002
FILE_ATTRIBUTE_SYSTEM = 0x00000004
FILE_ATTRIBUTE_DIRECTORY = 0x00000010
FILE_ATTRIBUTE_ARCHIVE = 0x00000020
FILE_ATTRIBUTE_DEVICE = 0x00000040
FILE_ATTRIBUTE_NORMAL = 0x00000080
FILE_ATTRIBUTE_TEMPORARY = 0x00000100
FILE_ATTRIBUTE_SPARSE_FILE = 0x00000200
FILE_ATTRIBUTE_REPARSE_POINT = 0x00000400
FILE_ATTRIBUTE_COMPRESSED = 0x00000800
FILE_ATTRIBUTE_OFFLINE = 0x00001000
FILE_ATTRIBUTE_NOT_CONTENT_INDEXED = 0x00002000
FILE_ATTRIBUTE_ENCRYPTED = 0x00004000
FILE_ATTRIBUTE_VIRTUAL = 0x00010000

# file flags
FILE_FLAG_BACKUP_SEMANTICS = 0x02000000
FILE_FLAG_DELETE_ON_CLOSE = 0x04000000
FILE_FLAG_NO_BUFFERING = 0x20000000
FILE_FLAG_OPEN_NO_RECALL = 0x00100000
FILE_FLAG_OPEN_REPARSE_POINT = 0x00200000
FILE_FLAG_OVERLAPPED = 0x40000000
FILE_FLAG_POSIX_SEMANTICS = 0x01000000
FILE_FLAG_RANDOM_ACCESS = 0x10000000
FILE_FLAG_SEQUENTIAL_SCAN = 0x08000000
FILE_FLAG_WRITE_THROUGH = 0x80000000

# impersonation level flags
SECURITY_ANONYMOUS = 0
SECURITY_IDENTIFICATION = 1
SECURITY_IMPERSONATION = 2
SECURITY_DELEGATION = 3

# security flags
SECURITY_CONTEXT_TRACKING = 0x01
SECURITY_EFFECTIVE_ONLY = 0x02

# Share Mode
FILE_SHARE_DELETE = 0x00000004
FILE_SHARE_READ = 0x00000001
FILE_SHARE_WRITE = 0x00000002

# creation disposition flags
CREATE_NEW = 1
CREATE_ALWAYS = 2
OPEN_EXISTING = 3
OPEN_ALWAYS = 4
TRUNCATE_EXISTING = 5

# access mask
GENERIC_READ = 0x80000000
GENERIC_WRITE = 0x40000000
GENERIC_EXECUTE = 0x20000000
GENERIC_ALL = 0x10000000

# error codes
ERROR_INVALID_PARAMETER = 87
ERROR_DISK_FULL = 112
ERROR_INVALID_NAME = 123
ERROR_DIR_NOT_EMPTY = 145
ERROR_NOT_LOCKED = 158
ERROR_ALREADY_EXISTS = 183
ERROR_EAS_DIDNT_FIT = 275
ERROR_EAS_NOT_SUPPORTED = 282
ERROR_FILE_EXISTS = 80
ERROR_FILE_NOT_FOUND = 2
INVALID_HANDLE_VALUE = 0xFFFFFFFF

# maximum  path length
MAX_PATH = 0x00000104
