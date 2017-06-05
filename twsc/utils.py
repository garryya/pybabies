#!/usr/bin/python

"""small usefull stuff
"""
__author__ = 'GarryY'
__version__ = '0.1'

import sys
import logging
import logging.handlers
import traceback
import threading
from datetime import datetime as dt
import pickle
import bz2 as ZIP
import socket


LOG = logging.getLogger('twsc')

EOS = b'#EOS#'


def setup_logging(logname,
                  logfile=None,
                  level=logging.DEBUG,
                  to_stdout=True,
                  log_start=True,
                  FMT='%(asctime)s - %(name)-6s - %(levelname)-6s - [%(filename)s:%(lineno)d] - %(message)s',
                  title='',
                  version=''):
    global LOG
    LOG = logging.getLogger(logname)
    logging.basicConfig(level=level, format=(FMT))
    rh = logging.handlers.RotatingFileHandler(logfile if logfile else './%s.log' % logname,
                                              maxBytes=50000000,
                                              backupCount=2)
    rh.setLevel(level)
    rh.setFormatter(logging.Formatter(FMT))
    LOG.addHandler(rh)
    LOG.propagate = to_stdout
    logging.getLogger("requests").setLevel(logging.WARNING)
    if log_start:
        LOG.info("\n***\n*** Logging started @ %s in %s\n*** Python %s %s\n***\n%s\n%s\n",
                 dt.now(), logfile, sys.version.replace('\n',''), sys.executable, title, version)
    return LOG


def handle_exception(log, x, *args, **dargs):
    pf = log.error if log and 'print' not in dargs else print
    pf('[T:{:X}] exception: {} {}'.format(threading.currentThread().ident,
                                          x,
                                          '({})'.format(args) if args else ''))
    if 'errmsg' in dargs:
        pf('\t\t{}'.format(dargs['errmsg']))
    stack = None
    if 'stack_trace' in dargs:
        stack = dargs['stack_trace']
    elif 'stack' in dargs and dargs['stack']:
        try:
            stack = traceback.format_exc()
        except:
            tb = traceback.format_stack()[:-1]
            stack = ''.join(tb)
    if stack:
        pf('[T:%x stack]\n%s' % (threading.currentThread().ident, stack))
    return stack



def _serialize(data, pickle_it=False, compress=False):
    data = pickle.dumps(data) if pickle_it else str(data).encode()
    if compress:
        data = ZIP.compress(data)
    return data


def _deserialize(data, pickle_it=False, compress=False):
    if compress:
        data = ZIP.decompress(data)
    return pickle.loads(data) if pickle_it else eval(data.decode())


def sockSend(host,
             port,
             data,
             verbose=False,
             ignore_error=False,
             serialize=True,
             compress=False):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        peerInfo = str(sock.getpeername())
        if serialize:
            data = _serialize(data, pickle_it=True, compress=compress)
        bs = sock.send(data)
        if verbose and LOG:
            LOG.debug('\t%s/%s bytes sent to %s:%d [[[%s...]]]' % (bs, len(data), host, port, str(data)[:64]))
        received = None
        sock.close()
        return peerInfo, received
    except socket.error as x:
        if not ignore_error and LOG:
            handle_exception(LOG, x, host, port, stack=False)
    except Exception as x:
        handle_exception(LOG, x, stack=True)
    finally:
        return None, None
