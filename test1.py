#!/usr/bin/python
"""
"""
__author__ = 'garryya'
__version__     = '0.1'

import sys
import os
import re

print sys.argv[1:]

#if len(sys.argv)<=1 or not os.path.exists(sys.argv[1]):
#    print 'not exists'
#    sys.exit(1)

from subprocess import Popen, PIPE

cmd = sys.argv[1]

print('** 1')
p = Popen([cmd], shell=True, stdout=PIPE, stderr=PIPE)

o, e = p.communicate()

print('e=%s\no=%s' % (e,o))




