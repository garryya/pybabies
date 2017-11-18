#!/grid/common/pkgs/python/v3.4.0/bin/python3 -B

from twisted.internet.protocol import Protocol, Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.threads import deferToThread
from twisted.internet import reactor, defer
import threading
from grutils import setup_logging, handle_exception, EMPTY_RESPONSE_HOLDER, addr2name
from grutils import _deserialize
import logging
from optparse import OptionParser
import uuid
from clt import the_file


LOG = logging.getLogger('srv')


parser = OptionParser()
parser.add_option('--port', '-p', dest='port', default=7777)
parser.add_option('--nocompress', dest='nocompress', action='store_true', default=False)
options, run_cmd = parser.parse_args()


class ReceiveStream(LineReceiver):
    compress = True
    verification_file = None
    def __init__(self):
        self.setRawMode()
        self.chunks = []

    def getpeer(self):
        return self.transport.getPeer()

    def collectedDataLen(self):
        return sum(len(c) for c in self.chunks)

    def connectionMade(self):
        #self.factory.clients.append(self)
        peer = self.getpeer()
        LOG.info('\tconnected from {}:{}'.format(peer.host, peer.port))
        self.chunks = []

    def rawDataReceived(self, data):
        peer = self.getpeer()
        self.chunks.append(data)
        LOG.info('\t\trecieved from {}:{} ---> {} / {}:{} / {}...'.format(
                                                       peer.host,
                                                       peer.port,
                                                       len(data),
                                                       len(self.chunks),
                                                       self.collectedDataLen(),
                                                       str(data)[:32]))

    def verify(self, file, buffer):
        return open(file, 'rb').read() == buffer

    def connectionLost(self, reason):
        peer = self.getpeer()
        data = b''.join(self.chunks)
        success = True
        try:
            data = _deserialize(data, do_pickle=True, do_compress=ReceiveStream.compress)
            if ReceiveStream.verification_file:
                assert self.verify(ReceiveStream.verification_file, data), 'Verification failed for {}'.format(the_file)
        except Exception as x:
            errmsg = 'failed deserializing stream: {}'.format(x)
            success = False
        LOG.info('\t{} from {}:{} ---> {} / {} / {}...'.format('SUCCESS' if success else 'CORRUPTED! ({})'.format(errmsg),
                                                       peer.host,
                                                       peer.port,
                                                       self.collectedDataLen(),
                                                       len(self.chunks),
                                                       str(data)[:32]))
        # self.transport.write(EMPTY_RESPONSE_HOLDER.encode())
        # self.factory.clients.remove(self)


######################################
######################################

try:
    LOG = setup_logging('srv', 'srv.log', level=logging.DEBUG, to_stdout=True)

    ReceiveStream.compress = not options.nocompress
    ReceiveStream.verification_file = the_file

    f = Factory()
    f.protocol = ReceiveStream
    reactor.listenTCP(options.port, f)
    reactor.run()

except KeyboardInterrupt:
    pass
except Exception as e:
    handle_exception(LOG, e, stack=True)
