#!/grid/common/pkgs/python/v3.4.0/bin/python3 -B

import sys
import threading
from grutils import setup_logging, sockSend, _serialize
from grutils import handle_exception, runcmdo, EMPTY_RESPONSE_HOLDER, opt_choice_validator
import traceback
import logging
from twisted.internet import reactor, protocol
from twisted.protocols.basic import LineReceiver


#the_file = '/lan/cva/debugger_user4/garryya/rd/zjob/packages/1.0/zjob-1.0.144-rhel-6.5-x86_64.tar.gz'
the_file = '/lan/cva/debugger_user4/garryya/rd/pt/build/exe.linux-x86_64-2.6/libpython2.6.so.1.0'
#the_file = 'disasm.py'
#the_file = 'aaa'

LOG = setup_logging('clt', 'clt.log', level=logging.DEBUG, to_stdout=True)

def tf(n, buffer, host, port, compress):
    tid = threading.currentThread().ident
    res = sockSend(host,
                   port,
                   buffer,
                   wait_for_response=False,
                   verbose=True,
                   timeout=None,
                   serialize=True,
                   do_compress=compress)
    LOG.debug('[CLT:%x]\t %6s --> %s', tid, n, str(res))


class SendStream(LineReceiver):
    compress = True
    def __init__(self):
        self.setRawMode()
        self._buffer = None

    def set_buffer(self, buffer):
        self._buffer = buffer

    def connectionMade(self):
        if self._buffer:
            data = _serialize(self._buffer, do_pickle=True, do_compress=SendStream.compress)
            bs = self.sendLine(data)
            LOG.debug('sent {}/{} --> {}...'.format(bs, len(data), data[:20]))
        self.transport.loseConnection()


class SendStreamFactory(protocol.ClientFactory):
    protocol = SendStream
    def __init__(self, buffer):
        self._buffer = buffer

    def buildProtocol(self, addr):
        p = protocol.ClientFactory.buildProtocol(self, addr)
        p.set_buffer(self._buffer)
        return p

    def clientConnectionFailed(self, connector, reason):
        LOG.error('connection refused: {}'.format(reason))

def tw_stream_send(buffer, host, port, compress=True):
    SendStream.compress = compress
    f = SendStreamFactory(buffer)
    f.protocol = SendStream
    reactor.callLater(0, reactor.connectTCP, host, port, f)


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
        parser.add_option('--twisted', dest='twisted', action='store_true', default=False)
        parser.add_option('--ttt',
                          dest='ttt',
                          type='str',
                          action='callback',
                          callback = opt_choice_validator,
                          callback_kwargs=dict(choices=['fuck', 'dick']),
                          default='',
                          help='aaaa')
        options, args = parser.parse_args()
        print('options={}\nargs={}'.format(options, args))

        buffer = open(options.file, 'br').read()

        if options.twisted:
            for i in range(1, options.n + 1):
                tw_stream_send(buffer, options.server, options.port, not options.nocompress)
            reactor.run()
        else:
            threads = [threading.Thread(target=tf,
                                        args=(i, buffer, options.server, options.port, not options.nocompress),
                                        name=str(i)) for i in range(1, options.n + 1)]
            assert threads
            [t.start() for t in threads]
            [t.join() for t in threads]

    except KeyboardInterrupt:
        reactor.stop()
    except Exception as e:
        LOG.error('Exception: %s', e)
        LOG.error(traceback.format_exc())

