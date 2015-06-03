from twisted.internet.defer import Deferred
from twisted.internet import reactor
import twisted.internet.threads

import threading

def thread_id():
    return threading.current_thread().name


def long_op(*args, **kwargs):
    print ' ' 
    print 'starting long_op ...'
    print '    thread id = ' + repr(thread_id())
    r = range(0,60)
    for i in r:
        print 'i = ' + str(i)
    print '    ... done'
    return sum(r) 

def long_op_result(res):
    print 'long_op_result = ' + repr(res)
    print '  moving to state 4'
    reactor.callLater(0.0, state_4)
    return

def test2(*args, **kwargs):
    print 'test2: '
    print '    ' + repr(args)
    print '    ' + repr(kwargs)
    return 

def test(x, *args, **kwargs):
    print 'x = ' + repr(x)
    for y in args:
        print 'y = ' + repr(y) 

    for k,v in kwargs.iteritems():
        print (repr(k),repr(v))

    print 'in dict form'
    print '    ' + repr(kwargs)
    test2(kwargs)
    return 

def state_err():
    print 'error_state'
    return

def state_1():
    reactor.callLater(0.0, state_2)

    print 'in state_1'

def state_2():
    reactor.callLater(0.0, state_3)

    print 'in state_2' 

def state_3():
    print 'in state_3' 
    print '   calling long_op on another thread'
    d = twisted.internet.threads.deferToThread(long_op)
    d.addCallback(long_op_result)
    print '   state_3 about to return'
    return

def state_4():
    print 'in state_4'
    reactor.stop()
    return

def main():
    print 'main'
    print '    thread_id = ' + repr(thread_id())

    # start with the initial state
    reactor.callLater(0.0, state_1)

#    print 'calling test2()'
#    test2(0, {'cat': 1, 'dog': 2})

    # start the reactor
    reactor.run()

if __name__ == '__main__':
    main()


