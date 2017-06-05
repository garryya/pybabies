#!/usr/bin/python3 -B

import logging
from optparse import OptionParser
from twisted.internet.protocol import Protocol, Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet import reactor, defer
from utils import setup_logging, handle_exception, _deserialize, EOS
from c import the_file


LOG = logging.getLogger('twsc')


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

    def dataReceived(self, data):
        LineReceiver.dataReceived(self, data)

    def getpeer(self):
        return self.transport.getPeer()

    def collectedDataLen(self):
        return sum(len(c) for c in self.chunks)

    def connectionMade(self):
        peer = self.getpeer()
        LOG.info('\tconnected from {}:{}'.format(peer.host, peer.port))
        self.chunks = []

    def rawDataReceived(self, data):
        peer = self.getpeer()
        LOG.info('\t\tgot raw from {}:{} ---> {} / {}:{} / {}...'.format(
                                                       peer.host,
                                                       peer.port,
                                                       len(data),
                                                       len(self.chunks),
                                                       self.collectedDataLen(),
                                                       str(data)[:32]))

        if len(data) > len(EOS)+2 and data[-len(EOS)-2:-2] == EOS:
            self.chunks.append(data[:-len(EOS)-2])
            self.finilize(peer)
            self.transport.loseConnection()
        else:
            self.chunks.append(data)

    def lineReceived(self, line):
        LOG.info('got line={}'.format(line))
        self.transport.write('got it!')

    def verify(self, file, buffer):
        return open(file, 'rb').read() == buffer

    def finilize(self, peer):
        LOG.info('\t\tfinilizing stream from {} ...'.format(peer))
        data = b''.join(self.chunks)
        success = True
        try:
            data = _deserialize(data, pickle_it=True, compress=ReceiveStream.compress)
            if ReceiveStream.verification_file:
                assert self.verify(ReceiveStream.verification_file, data), 'Verification failed for {}'.format(the_file)
        except Exception as x:
            errmsg = 'failed deserializing stream: {}'.format(x)
            success = False
        LOG.info(
            '\t\t{} from {}:{} ---> {} / {} / {}...'.format('SUCCESS' if success else 'CORRUPTED! ({})'.format(errmsg),
                                                            peer.host,
                                                            peer.port,
                                                            self.collectedDataLen(),
                                                            len(self.chunks),
                                                            str(data)[:32]))

    def connectionLost(self, reason):
        if self.chunks:
            self.finilize(self.getpeer())

######################################
######################################

try:
    LOG = setup_logging('twsc', 's.log', level=logging.DEBUG, to_stdout=True)

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
