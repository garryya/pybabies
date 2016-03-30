#!/usr/bin/python

from os import path
import sys
import getopt
from grutils import runcmdo, TermColors as TC
from configobj import ConfigObj

CURRENT_DIR = os.path.abspath(os.path.split(__file__)[0])
BUILD_DIR = STAGE_DIR = os.path.join(CURRENT_DIR, 'build/exe.linux-x86_64-2.6')
LOG = os.path.join(CURRENT_DIR, 'deploy.log')

print sys.argv[1:]

designPath = None
n_jobs = 1

try:
    opts, args = getopt.getopt(sys.argv[1:], 's', ['design=', 'array=','server-host=','restart','build-only'])
    print('args: %s | %s' % (opts,args))
except getopt.GetoptError as e:
    print('Exception %s' % e)
    sys.exit(2)

for opt, arg in opts:
    if opt in ('--design'):
        designPath =


designAnchor = path.join(designPath, 'dbFiles/qtdesign.et3confg')
LOG.info('* Verifying design (%s)...' % designAnchor)
return designAnchor if path.exists(designAnchor) else None


# copy



