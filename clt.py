#!/grid/common/pkgs/python/v3.4.0/bin/python3 -B

import sys
import threading
from grutils import setup_logging, sockSend, _serialize, handle_exception, runcmdo, EMPTY_RESPONSE_HOLDER
import traceback
import logging
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver


the_file = '/lan/cva/debugger_user4/garryya/rd/zjob/packages/1.0/zjob-1.0.144-rhel-6.5-x86_64.tar.gz'
#the_file = '/lan/cva/debugger_user4/garryya/rd/pt/build/exe.linux-x86_64-2.6/datetime.so'
#the_file = 'disasm.py'
#the_file = 'aaa'

LOG = setup_logging('clt', 'clt.log', level=logging.DEBUG, to_stdout=True)

def tf(n):
    tid = threading.currentThread().ident

    data = open(options.file, 'br').read()

    res = sockSend(options.server,
                   options.port,
                   data,
                   wait_for_response=False,
                   verbose=True,
                   timeout=None,
                   serialize=True,
                   compress=False)

    LOG.debug('[CLT:%x]\t %6s --> %s', tid, n, str(res))


class SendStream(LineReceiver):
    compress = True
    def __init__(self):
        self.setRawMode()

    def connectionMade(self):
        data = open(options.file, 'br').read()
        data = _serialize(data, pickle_it=True, compress=SendStream.compress)
        bs = self.sendLine(data)
        LOG.debug('sent {}/{} --> {}...'.format(bs, len(data), data[:20]))
        self.transport.loseConnection()

class SendStreamFactory(protocol.ClientFactory):
    protocol = SendStream
    def clientConnectionFailed(self, connector, reason):
        print("Connection failed - goodbye!")
        reactor.stop()
        sys.exit(1)
    def clientConnectionLost(self, connector, reason):
        print("Connection lost - goodbye!")
        reactor.stop()
        sys.exit(1)



if __name__ == '__main__':
    try:

        from optparse import OptionParser

        parser = OptionParser()
        parser.add_option('--server', dest='server', default='127.0.0.1')
        parser.add_option('--port', '-p', dest='port', default=7777)
        parser.add_option('-n', dest='n', default=1, type=int)
        parser.add_option('-s', dest='size', default=4096, type=int)
        parser.add_option('--file', '-f', dest='file', default=the_file)
        parser.add_option('--nocompress', dest='nocompress', action='store_true', default=False)
        options, run_cmd = parser.parse_args()

        SendStream.compress = not options.nocompress

        f = protocol.ClientFactory()
        f.protocol = SendStream

        for i in range(1, options.n + 1):
            reactor.callLater(0, reactor.connectTCP, options.server, options.port, f)
        #reactor.callLater(5, reactor.stop)
        reactor.run()

    except KeyboardInterrupt:
        reactor.stop()
    except Exception as e:
        LOG.error('Exception: %s', e)
        LOG.error(traceback.format_exc())

