# command_processor.py
# A way to decouble a request from a request implementation

from twisted.internet.defer import Deferred
from twisted.internet import reactor
import twisted.internet.threads

import threading

class command_processor(object):
    def __init__(self)
        pass

    def add_command(self, cmd, proc):
        pass

    def queue_command(self, cmd):
        pass
