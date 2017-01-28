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
from grutils import DeferredLockSet

#print sys.argv[1:]


def  StairCase(n):
    fmt = '{:>%d}' % n
    for i in range(1, n+1):
        print(fmt.format('#'*i))
#StairCase(int(sys.argv[1]))

def _finally():
    try:
        raise KeyError
        #a = int('aaaaa')
        print(1)
        os.exit(0)
    except Exception as e:
        print
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



handlers = {'X': dict(delay=1, ended=False),
            'U': dict(delay=1, ended=False),
            'Y': dict(delay=1, ended=False)}


def _t(s, delay=1, n=3):
    for _ in range(n):
        print(s)
        time.sleep(delay)
    return s

sem = defer.DeferredSemaphore(len(handlers))

def _tcb(h, locks):
    print('{} ended'.format(h))
    handlers[h]['ended'] = True
    #if all(v['ended'] for v in handlers.values()):
    #    reactor.stop()
    locks.release(key=h)

def _stop(r, locks):
    print('STOP: {}'.format(r))
    locks.release()
    reactor.stop()

def test_twisted():
    #[sem.acquire() for _ in handlers]
    #[deferToThread(_t, h, delay=v['delay']).addCallback(_tcb, sem) for h, v in handlers.items()]
    #reactor.callLater(1, defer.DeferredList([sem.acquire() for _ in range(len(handlers)+0)]).addCallback, _stop)

    locks = DeferredLockSet(keys=handlers.keys(), acquired=True)
    [deferToThread(_t, h, delay=v['delay']).addCallback(_tcb, locks) for h, v in handlers.items()]
    reactor.callLater(1, locks.acquire().addCallback, _stop, locks)

    reactor.run()

try:

    test_argparser()

    #test_twisted()

except KeyboardInterrupt:
    pass
except Exception as e:
    print(traceback.format_exc(e))