#!/usr/bin/env python

# Generate PyXB binding classes from schemas.

import os
import glob
import optparse


def generateVersion(schemaFile, destfolder="./d1_common/types/generated"):
  '''given the DataONE types schema, generates a version module that 
  contains version information about the file.
  '''
  from xml.etree.ElementTree import parse
  import pysvn
  import datetime

  cli = pysvn.Client()
  svninfo = cli.info(schemaFile)
  svnrev = str(svninfo.revision.number)
  svnpath = svninfo.url
  xml = parse(schemaFile)
  version = xml.getroot().attrib["version"]
  tstamp = datetime.datetime.utcnow().isoformat()
  fdest = file(os.path.join(destfolder, "version.py"), "w")
  fdest.write(
    """#This file is automatically generated. Manual edits will be erased.

# When this file was generated
TIMESTAMP="%s"

# Path of the schema used in the repository
SVNPATH="%s"

# SVN revision of the schema that was used
SVNREVISION="%s"

# The version tag of the schema
VERSION="%s"
  
  """ % (tstamp, svnpath, svnrev, version)
  )
  fdest.close()


def main():
  # Command line opts.
  parser = optparse.OptionParser()
  # The default location for the schemas relative to d1_common_python if both were checked out as part of cicore.
  parser.add_option(
    '-s',
    '--schemas',
    dest='schema_path',
    action='store',
    type='string',
    default='./d1_schemas'
  )
  parser.add_option(
    '-t',
    '--types',
    dest='types_generated_path',
    action='store',
    type='string',
    default='./d1_common/types/generated'
  )
  parser.add_option(
    '-b',
    '--binding',
    dest='types_generated_binding',
    action='store',
    type='string',
    default='dataoneTypes.xsd'
  )

  (opts, args) = parser.parse_args()

  if not os.path.exists(opts.types_generated_path):
    print 'This script should be run from ./d1_common_python/src'
    exit()

  # pyxbgen sometimes does not want to overwrite existing binding classes.
  try:
    os.unlink(os.path.join(opts.types_generated_path, opts.types_generated_binding))
  except:
    pass

  # Generate.
  args = []

  args.append('--binding-root=\'{0}\''.format(opts.types_generated_path))
  #args.append('--location-prefix-rewrite=\'https://repository.dataone.org/software/cicore/trunk/schemas/={0}\''.format(opts.schema_path))

  print opts.types_generated_binding
  for xsd in glob.glob(os.path.join(opts.schema_path, '*.xsd')):
    print xsd
    generateVersion(xsd)
    #if os.path.basename(xsd) not in (opts.types_generated_binding):
    #  continue
    args.append(
      '-u \'{0}\' -m \'{1}\''.format(
        xsd, os.path.splitext(
          os.path.basename(xsd)
        )[0]
      )
    )

  print str(args)

  #if len(args) <= 2:
  #  print 'Didn\'t find any schemas at \'{0}\''.format(opts.schema_path)
  #  exit()

  cmd = 'pyxbgen {0}'.format(' '.join(args))
  print(cmd)
  os.system(cmd)


if __name__ == '__main__':
  main()
