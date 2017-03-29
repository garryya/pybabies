#!/grid/common/pkgs/python/v3.4.0/bin/python3
"""
"""
__author__ = 'garryya'
__version__     = '0.1'

import sys
import os
import re
from optparse import OptionParser, OptionGroup, SUPPRESS_HELP
import argparse
import traceback
from collections import OrderedDict, namedtuple
import json
from twisted.internet import reactor, error, defer
from twisted.internet.threads import deferToThread
import time
from grutils import DeferredLockSet, handle_exception, kill_process, get_fqdn

#print sys.argv[1:]


def  StairCase(n):
    fmt = '{:>%d}' % n
    for i in range(1, n+1):
        print(fmt.format('#'*i))
#StairCase(int(sys.argv[1]))

def _finally():
    try:
        # raise KeyError
        #a = int('aaaaa')
        print(1)
        #os.exit(0)
    except Exception as e:
        print('EXC!!')
    finally:
        print('something is wrong')


def test_optparser():
    parser = OptionParser()
    g1 = OptionGroup(parser, 'G1')
    g2 = OptionGroup(parser, 'G2')
    #parser.add_option("-a", "--action", dest='action', action='store_true', default='a', help="aaaaaa what to do")
    g1.add_option("--l1", dest='l1', action='store_true', default='l1', help="l1")
    g1.add_option("-b", dest='bb', action='store_true', default='bb', help="bb")
    g2.add_option("--l2", dest='l2', action='store_true', default='l2', help="l2")
    parser.add_option_group(g1)
    parser.add_option_group(g2)
    opts, args = parser.parse_args()
    print(opts, args)
    pass

def test_argparser():
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group()
    parser.add_argument("-a", "--action", dest='action', action='store_true', default='a', metavar=argparse.SUPPRESS)
    parser.add_argument("-b", dest='bb', action='store_true', default='bb', help="bb")
    g.add_argument("--l1", dest='l1', action='store_true', default='l1', help="l1")
    g.add_argument("--l2", dest='l2', action='store_true', default='l2', help="l2")
    opts, args = parser.parse_args()
    print(opts, args)
    pass


def dec(o):
    from grutils import decob
    #print('{:_>16!s} --> {:_<!s}'.format(o, decob(o)))
    o_ = decob(o)
    print('{!s} --> {} {!s}'.format(o, type(o_), o_))


def test_dec():
    dec('abc')
    dec(b'abc')
    dec({b'a':1234, b'b':b'b', 'c':[1, 2, b'aaa', {1:1, 2:'2', 3:b'3', '3':b'3', b'4':b'4'}]})
    dec([b'abc', '123', b'456'])
    dec(set([b'abc', '123', b'456']))
    dec((b'abc', '123', b'456'))


def tb(e):
    tb = traceback.format_exception(type(e), e)
    print(tb)


def test_andy():
    inpfile = sys.argv[1]
    html = open('template.html').read()
    s = ''
    with open(inpfile) as f:
        for l in f.readlines():
            s += '<h2>{}</h2>\n'.format(l)
    html = html.replace('%%NETS%%', s)
    with open(inpfile+'.html','w') as f:
        f.write(html)





#############################################
#############################################


class Status:
    __status__ = True
    def __init__(self, name, id, text=None):
        self.id = id
        self.name = name
        self.text = text
    def __str__(self):
        return self.text
    def __repr__(self):
        return '({}): {}'.format(self.id, self.text)
    def format(self, add=None):
        return '{!r}{}'.format(self, '\n{}'.format(add) if add else '')
    def success(self):
        return self.id == 0

class StatusMap:
    def __init__(self, **status_list):
        for s, sv in status_list.items():
            if not isinstance(sv, tuple):
                sv = (sv, s)
            setattr(self, s, Status(s, *sv))
    def enumerate(self):
        return [getattr(self, a) for a in dir(self) if hasattr(getattr(self, a), '__status__')]
    def __str__(self):
        return '\n'.join([str(s) for s in self.enumerate()])


def test_status():
    ss = StatusMap(
        S1=1,
        S2=2,
        S3=(3,'SSS#3'),
    )

    print(ss)
    print('{0!r}'.format(ss.S1))
    print('{}'.format(ss.S1.format()))


def test_meta():
    JobSubproc_ = namedtuple('JobSubproc_', ['id', 'killf', 'verbose'])

    class JobSubproc(JobSubproc_):
        def __init__(self, id, killf, verbose):
            JobSubproc_.__init__(id, killf, verbose)
            self.kill = self.kill
        def __new__(cls, id, killf, verbose):
            return JobSubproc_.__new__(JobSubproc_, id, killf, verbose)
        def kill(self):
            return self.killf(self.id, verbose=self.verbose)

    class OSJobSubproc(JobSubproc):
        def __init__(self, pid, verbose=True):
            JobSubproc.__init__(id=pid, killf=kill_process, verbose=verbose)
        def __new__(cls, pid, verbose=True):
            return JobSubproc.__new__(cls, id=pid, killf=kill_process, verbose=verbose)

    class DRMJobSubproc(JobSubproc):
        def __init__(self, job_id, drm_obj, verbose=True):
            JobSubproc.__init__(id=job_id, killf=drm_obj.kill, verbose=verbose)
        def __new__(cls, job_id, drm_obj, verbose=True):
            return JobSubproc.__new__(cls, id=job_id, killf=drm_obj.kill, verbose=verbose)

    _JobSubprocSet = namedtuple('JobSubprocSet', ['os', 'drm'])
    JobSubprocSet = _JobSubprocSet(os=OSJobSubproc, drm=DRMJobSubproc)

    j1 = OSJobSubproc(-1)
    print(j1)
    j2 = DRMJobSubproc(-1, os)
    print(j2)

    # j1.kill()
    j2.kill()



from functools import wraps

def decor(dec_arg):
    def w(f):
        @wraps(f)
        def ww(*args, **dargs):
            dargs['add1'] = 'AAD1'
            dargs['DECARG'] = dec_arg
            return f(*args, **dargs)
        return ww
    return w

@decor('DECARG111')
def test_decorator(*args, **dargs):
    print('F({}, {})'.format(args, dargs))

#######################



try:

    print(sys.executable)
    print(sys.argv)

    print(os.path.dirname(os.path.realpath(__file__)))

    print(get_fqdn())

    #test_argparser()

    # _finally()

    # test_meta()

    # test_cast()

    test_decorator(1, 2, 3, 'QUQU', sss='SS')

    pass

except KeyboardInterrupt:
    pass
except Exception as x:
    handle_exception(None, x, stack=True)