#!/usr/bin/python

import sys
sys.path.append('./tools/cx_Freeze-4.3.4-py2.6-linux-x86_64.egg')

from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
buildOptions = dict(
    packages = [],
    excludes = [],
    include_files = ['test1-new.html'] )

base = 'Console'

executables = [
        Executable('cakex.py', base=base),
        Executable('pex.py', base=base),
]

sys.argv.append('build')
setup(name='pt',
      version='1.0',
      description='',
      options=dict(build_exe = buildOptions),
      executables=executables, requires=['twisted', 'configobj', 'simplejson',])

import os
for e in executables:
    os.system('chmod +x %s' % e.targetName)

