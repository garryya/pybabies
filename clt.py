#!/usr/bin/python -B

import threading
from grutils import setup_logging, sockSend, handle_exception, runcmdo, EMPTY_RESPONSE_HOLDER
import traceback
import logging
from optparse import OptionParser


parser = OptionParser()
parser.add_option('--server',dest='server', default='localhost')
parser.add_option('--port', '-p', dest='port', default=7777)
parser.add_option('-n', dest='n', default=1, type=int)
parser.add_option('-s', dest='size', default=4096, type=int)
options, run_cmd = parser.parse_args()

LOG = setup_logging('clt', 'clt.log', level=logging.DEBUG, to_stdout=True)


def tf(n):
    tid = threading.currentThread().ident
    #LOG.debug('[CLT:%x] sending: %s', tid, n)

    data = 'X' * options.size * options.n
    data = data.encode()
    res = sockSend(options.server, options.port, data, wait_for_response=True, verbose=True, timeout=None, serialize=False)

    #sres = res[1]
    #ns = str(n)
    #lns = len(ns)
    #check = all([ns==sres[i*lns:(i+1)*lns] for i in range(n)])

    #LOG.debug('[CLT:%x]\t %6s --> %5s\t%s', tid, n, check, sres[:32])
    LOG.debug('[CLT:%x]\t %6s --> %s', tid, n, str(res))


N = 1
try:
    threads = [threading.Thread(target=tf, args=(i,), name=str(i)) for i in range(1, N+1)]
    assert threads
    [t.start() for t in threads]
    [t.join() for t in threads]

except KeyboardInterrupt:
    pass
except Exception as e:
    LOG.error('Exception: %s', e)
    LOG.error(traceback.format_exc())

