#!/usr/bin/python -B

from twisted.internet.protocol import Protocol, Factory
from twisted.protocols.basic import LineReceiver
from twisted.internet.threads import deferToThread
from twisted.internet import reactor, defer
import threading
from grutils import setup_logging, handle_exception, EMPTY_RESPONSE_HOLDER, addr2name, post_send
import logging
import time

LOG = logging.getLogger('srv')

class server(Protocol):
    def __init__(self):
        pass

    #@defer.inlineCallbacks
    def dataReceived(self, data):
        #data = post_send(data)
        data = data.decode('utf-8')
        LOG.info('[SRV] data recieved from %s: %s... (l=%d) ...' %
                 (addr2name(self.transport.getPeer().host), str(data)[:32], len(data)))
        self.transport.write(EMPTY_RESPONSE_HOLDER.encode())

class serverX(LineReceiver):
    def __init__(self):
        self.setRawMode()

    # def dataReceived(self, data):
    #     data = data.decode('utf-8')
    #     LOG.info('data recieved from %s: %s... (l=%d) ...' %
    #              (addr2name(self.transport.getPeer().host), str(data)[:32], len(data)))
    #     self.transport.write(EMPTY_RESPONSE_HOLDER.encode())
    #
    #@defer.inlineCallbacks
    def rawDataReceived(self, data):
        #data = post_send(data)
        data = data.decode('utf-8')
        LOG.info('raw  recieved from %s: %s... (l=%d) ...' %
                 (addr2name(self.transport.getPeer().host), str(data)[:32], len(data)))
        self.transport.write(EMPTY_RESPONSE_HOLDER.encode())


######################################
######################################

try:
    LOG = setup_logging('srv', 'srv.log', level=logging.DEBUG, to_stdout=True)

    f = Factory()
    f.protocol = serverX
    reactor.listenTCP(7777, f)
    reactor.run()

    #reactor.callLater(1, serverObject()._update_status, event='#START#')

except KeyboardInterrupt:
    pass
except Exception as e:
    handle_exception(LOG, e)
