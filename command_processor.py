# command_processor.py
# A way to decouple a request from a request implementation

from twisted.internet.defer import Deferred
from twisted.internet import reactor
import twisted.internet.threads

import threading

class command_processor(object):
    def __init__(self, evt_loop):
        # create an empty dictionary of events
        # will be populated by add_command()
        # each entry is a key,value pair where the
        # key is the name of the comamand and the value is a 
        # list of functions to execute in response to
        # the command
        #
        # evt_loop is the (a?) reactor
        self._procs = {}
        self._reactor = evt_loop
        self._queue = []
        pass

    def _on_event(self, args):
        if len(self._queue) == 0:
            print '_on_event() there is nothing in the queue'
            return []
        else:
            cmd,self._queue = self._queue[0],self._queue[1:]
            return cmd

    def _on_event_results(self, args):
        print '_on_event_results'
        print '   args = ' + repr(args)
        c = args[0]
        a = args[1]
        for proc in self._procs[c]:
            proc(a)
        return

    def add_command(self, cmd, proc):
        if cmd in self._procs:
            self._procs[cmd].append(proc)
        else:
            # this is the first proc in the list
            self._procs[cmd] = [proc]
        return

    def queue_command(self, cmd, args):
        self._queue.append([cmd,args])
        d = twisted.internet.threads.deferToThread(self._on_event,args)
        d.addCallback(self._on_event_results)
        return

    def dump_commands(self):
        for proc in self._procs:
            print 'proc: ' + proc
            print 'cmds: ' + repr(self._procs[proc])
        return

    def run(self):
        self._reactor.run()
        return

    def stop(self):
        self._reactor.stop()


# the sole command processor
cp = command_processor(reactor)

# our state machine
# so sad it will never see the light of day :(
def cmd1_1(args):
    print 'cmd1_1' + '(' + repr(args) + ')'
    cp.queue_command('cmd2', {'cat': 12, 'dog': 16})
    return

def cmd1_2(args):
    print 'cmd1_2' + '(' + repr(args) + ')'
    # cp.queue_command('cmd2', {'cat': 13, 'dog': 17})
    return

def cmd2_1(args):
    print 'cmd2_1' + '(' + repr(args) + ')'
    cat = args['cat']
    dog = args['dog']
    if cat > 0:
        cp.queue_command('cmd2', {'cat': cat - 1, 'dog': dog})
    else:
        cp.stop()
    return;

def main():
    cp.add_command('cmd1', cmd1_1)
    cp.add_command('cmd1', cmd1_2)
    cp.add_command('cmd2', cmd2_1)

    cp.queue_command('cmd1', {'a': 1, 'b': 2})

    cp.run()
    return

if __name__ == "__main__":
    main()
