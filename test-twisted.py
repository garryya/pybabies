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

handlers = {'X': dict(n=5, delay=1, ended=False),
            'U': dict(n=3, delay=1, ended=False),
            'Y': dict(n=3, delay=1, ended=False)}


def _t(s, delay=1, n=3):
    for _ in range(n):
        print(s)
        time.sleep(delay)
    return s

sem = defer.DeferredSemaphore(len(handlers))

def _tcb(h, locks=None):
    print('{} ended'.format(h))
    handlers[h]['ended'] = True
    if locks:
        locks.release(key=h)

@defer.inlineCallbacks
def _stop(locks):
    print('STOP 1: {}'.format(''))
    yield locks.acquire()
    print('STOP 2: {}'.format(''))
    yield locks.release()
    reactor.stop()

def test_twisted_lock():
    #[sem.acquire() for _ in handlers]
    #[deferToThread(_t, h, delay=v['delay']).addCallback(_tcb, sem) for h, v in handlers.items()]
    #reactor.callLater(1, defer.DeferredList([sem.acquire() for _ in range(len(handlers)+0)]).addCallback, _stop)

    locks = DeferredLockSet(keys=handlers.keys(), acquired=True)
    [deferToThread(_t, h, delay=v['delay'], n=v['n']).addCallback(_tcb, locks) for h, v in handlers.items()]
    #reactor.callLater(0, locks.acquire().addCallback, _stop, locks)
    reactor.callLater(0, _stop, locks)
    reactor.run()


@defer.inlineCallbacks
def test_twisted_multi_deferred():
    print('starting...')
    yield defer.DeferredList([deferToThread(_t, h, delay=v['delay'], n=v['n']).addCallback(_tcb) for h, v in handlers.items()])
    print('\ndone')
    reactor.stop()

@defer.inlineCallbacks
def f1():
    yield
    return 1, 2

def test_t():
    a, b = yield f1()
    print(a, b)


@staticmethod
def sleep(t):
    d = Deferred()
    reactor.callLater(t + 1, d.callback, None)
    # d.addCallback(reactor.callLater, t)
    return d


@inlineCallbacks
def wait_for_empty(self, somedata):
    while (True):
        LOG.debug('XXX wating: {}'.format(somedata))
        yield handle_WTF_FREE_EMULATORS.sleep(1)
        if not somedata:
            break
    returnValue(None)


#######################

try:

    print(sys.executable)
    print(sys.argv)
    print(os.path.dirname(os.path.realpath(__file__)))
    print(get_fqdn())
    print('+++++++')

    #test_twisted_multi_deferred()
    test_t()

    reactor.run()

except KeyboardInterrupt:
    pass
except Exception as x:
    handle_exception(None, x, stack=True)