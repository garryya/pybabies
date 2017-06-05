#!/usr/bin/python3 -B

import os
import sys
import logging
from twisted.internet import reactor, protocol, error, defer, endpoints
from twisted.protocols.basic import LineReceiver
from utils import setup_logging, handle_exception, _serialize, EOS, sockSend
import readline

LOG = setup_logging('twsc', 'c.log', level=logging.DEBUG, to_stdout=True)


the_file = None


class SendStream(LineReceiver):
    compress = True
    def __init__(self, f):
        self.f = f
        self.setRawMode()
    def connectionMade(self):
        self.send(self.f.buffer)
    @defer.inlineCallbacks
    def send(self, buffer):
        LOG.info('P::sending {} bytes'.format(len(self.f.buffer)))
        if buffer:
            data = _serialize(buffer, pickle_it=True, compress=SendStream.compress)
            self.sendLine(data)
            LOG.debug('\tsent {}b / {}...'.format(len(data), data[:20]))
            yield self.sendLine(EOS)
    def rawDataReceived(self, data):
        LOG.info('\treceived: {}'.format(data))


class SendStreamFactory(protocol.ClientFactory):
    def __init__(self, buffer):
        self.buffer = buffer
    def buildProtocol(self, addr):
        LOG.debug('building protocol {} ...'.format(addr))
        p = SendStream(self)
        return p
    def clientConnectionFailed(self, connector, reason):
        LOG.error('connection refused: {}'.format(reason))
        reactor.stop()



@defer.inlineCallbacks
def main_loop():
    while True:
        fname = input('* enter file name or q[uit]: ')
        if not fname:
            fname = __file__
        if 'quit'.startswith(fname.strip().lower()):
            reactor.stop()
            break
        global the_file
        the_file = fname
        if not os.path.exists(the_file):
            LOG.info('\tfile not found {}'.format(the_file))
            continue
        with open(fname, 'br') as f:
            buffer = f.read()
            try:
                LOG.info('\tsending {} ...'.format(fname))
                if not options.twisted:
                    yield defer.maybeDeferred(sockSend,
                                                options.server,
                                                options.port,
                                                buffer,
                                                verbose=True,
                                                serialize=True,
                                                compress=not options.nocompress)
                else:
                    point = endpoints.TCP4ClientEndpoint(reactor, options.server, options.port)
                    yield point.connect(SendStreamFactory(buffer))
            except Exception as x:
                LOG.error('Exception: {}'.format(x))




if __name__ == '__main__':
    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option('--server', dest='server', default='127.0.0.1')
    parser.add_option('--port', '-p', dest='port', default=7777)
    parser.add_option('--nocompress', dest='nocompress', action='store_true', default=False)
    parser.add_option('--twisted', dest='twisted', action='store_true', default=False)
    options, args = parser.parse_args()
    LOG.info('options={}\nargs={}\n'.format(options, args))

    SendStream.compress = not options.nocompress
    try:
        reactor.callLater(0, main_loop)
        reactor.run()
    except Exception as x:
        handle_exception(LOG, x, stack=True)
