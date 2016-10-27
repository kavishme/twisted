from __future__ import print_function

from pprint import pformat

from twisted.internet import reactor
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.web.client import Agent
from twisted.web.http_headers import Headers
from twisted.internet.defer import gatherResults
agent = Agent(reactor)
count = 0

d = agent.request(
    'GET',
    'http://google.in/',
    Headers({'User-Agent': ['Twisted Web Client Example']}),
    None)

d2 = agent.request(
    'GET',
    'http://google.com/',
    Headers({'User-Agent': ['Twisted Web Client Example']}),
    None)

d3 = agent.request(
    'GET',
    'http://google.co.uk/',
    Headers({'User-Agent': ['Twisted Web Client Example']}),
    None)

# class BeginningPrinter(Protocol):
#     def __init__(self, finished):
#         self.finished = finished
#         self.remaining = 1024 * 10

#     def dataReceived(self, bytes):
#         if self.remaining:
#             display = bytes[:self.remaining]
#             print('Some data received:')
#             print(display)
#             self.remaining -= len(display)

#     def connectionLost(self, reason):
#         print('Finished receiving body:', reason.getErrorMessage())
#         self.finished.callback(None)


def cbShutdown(ignored):
    print('Shutdown')
    reactor.stop()

def cbResponse(ignored):
    print('Response received')

def cbRequest(response):
    # print('Response version:', response.version)
    # print('Response code:', response.code)
    # print('Response phrase:', response.phrase)
    # print('Response headers:')
    # print(pformat(list(response.headers.getAllRawHeaders())))

    print(repr(response))
    #finished = Deferred()
    #response.deliverBody(BeginningPrinter(finished))
    #return finished

d.addCallback(cbRequest)
d2.addCallback(cbRequest)
d3.addCallback(cbRequest)


# class FireWhenAllFinish(Deferred):
#     def __init__(self, deferreds):
#         self.deferreds = deferreds
#         self.finishedCount = 0
#         if not self.deferreds:
#             self.callback()
#         for d in self.deferreds:
#             self.addCallbacks(self._cbDeferred, self._ebDeferred)
#     def _cbDeferred(self, result):
#         self.finishedCount += 1
#         if self.finishedCount == len(self.deferreds):
#             reactor.stop()
#             #self.callback()
#     def _ebDeferred(self, failure):
#         if not self.called: # this property is True if callback()/errback() has already been called
#             self.failed = True
#             reactor.stop()
#             #self.errback()

# defferShutdown = FireWhenAllFinish([d,d2,d3])
# defferShutdown.addBoth(cbShutdown)

finaldefer = gatherResults([d,d2,d3])
finaldefer.addBoth(cbShutdown)

reactor.run()