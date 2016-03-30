#!/usr/bin/python

import os
import sys
import pexpect
import traceback


try:

    os.environ['GRS_HOME'] = '/lan/cva/debugger_user3/eugene/tools/parasoft/dtp/grs'
    os.environ['PST_HOME'] = '/lan/cva/debugger_user3/eugene/tools/parasoft/dtp'

    pxp = pexpect.spawn('/lan/cva/debugger_user3/eugene/tools/parasoft/dtp/bin/dtpconsole.sh', timeout=None)
    pxp.expect(['(.*)Choose one : ', pexpect.EOF, pexpect.TIMEOUT])
    print(pxp.before)
    print(pxp.after)
    pxp.sendline('1')
    pxp.expect(['(.*)Choose one : ', pexpect.EOF, pexpect.TIMEOUT])
    print(pxp.before)
    print(pxp.after)
    pxp.sendline('1')
    pxp.expect(['(.*)Choose one : ', pexpect.EOF, pexpect.TIMEOUT])
    print(pxp.before)
    print(pxp.after)


except KeyboardInterrupt,  e:
    pass
except Exception,  e:
    print(e)
    traceback.print_exc()


