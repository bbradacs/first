from twisted.internet.defer import Deferred
from twisted.internet import reactor
from twisted.internet import threads

import threading
import random

# return represention of the current thread
def thread_id():
    return threading.current_thread().name

# create a random number between 1 .. 100 inclusive for testing
random.seed()
def random_arg():
    val = random.randint(1,100) 
    return val

# generate a random arg; if it is <= val then retrun the
# number, otherwise raise an exception
def run_this_later(max_val):
    print 'run_this_later: ' + repr(max_val) 
    print '    thread = ' + thread_id()
    val = random_arg()
    print '    val = ' + repr(val)
    if val <= max_val:
        return val
    else:
        raise Exception('did not get a value less than ' + repr(max_val))
    return 

def test_proc(max_val):
    print 'test_proc: ' + repr(max_val)
    d = threads.deferToThread(run_this_later, max_val)
    return d    
    

# attempt_n() will attempt to execute the provided function n
# times.  proc is a function that returns a deferred, args is the
# argument of proc, kwargs make up the keyword arguments of proc,
# and num_attempts is how many times you want to attempt to call
# proc before giving up
def attempt_n(num_attempts, proc, *args, **kwargs):

    # num_attempts must be at least one -- how to properly enforce
    # this?  raise an exception?

    d = Deferred()
    
    def on_success(result):
        d.callback(result) 
        return

    def on_failure(err, num_attempts):
        if num_attempts < 1:
            d.errback(err)
        else:
            # asynchronously call proc()
            _d = proc(*args, **kwargs)
            _d.addCallback(on_success)
            _d.addErrback(on_failure, num_attempts - 1)
        return

    # asynchronously call proc() and wire up our callback / errback
    # to the Deferred it returns
    _d = proc(*args, **kwargs)
    _d.addCallback(on_success)
    _d.addErrback(on_failure, num_attempts - 1)
   
    # return the deferred we created to the caller 
    return d 

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
    print ' '

    # start with the initial state
#    reactor.callLater(0.0, state_1)

#    print 'calling test2()'

    # start the reactor

    def s(args):
        print 'success! ' + repr(args)
        return

    def f(err):
        print 'fail! ' + str(err) 
        return

    def stop(_):
        print 'stop()'
        reactor.stop()
        return

    print 'about to call attempt_n()'
    d = attempt_n(5, test_proc, 10)
    print 'after calling attempt_n()'
    print 'about to call addCallbacks()'
    d.addCallbacks(s, f)
    d.addBoth(stop)
    print 'after calling addCallbacks()'

    print 'about to call reactor.run()'
    reactor.run()

    print 'the reactor has stopped, now play with Deferred'
    print ' '

    print 'creating a deferred'
    d = Deferred()

    print 'calling d.callback("foo")'
    d.callback('foo')

    print 'adding a callback'
    def cb(result):
        print 'result = ' + result
    d.addCallback(cb)

    def f(x):
        return x + 1
    def g(x):
        return x - 1

    f = g
    print f(33)
    f = f
    print f(36)
    
    return


if __name__ == '__main__':
    main()


