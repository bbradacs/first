import os
import sys
import functools

class A(object):
    # avoid using a dictionary to store member variables
    # curiously in this case the slots version takes up more space
    #__slots__ = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    def __init__(self, a):
        self.a = a
        self.b = a
        self.c = a
        self.d = a
        self.e = a
        self.f = a
        self.g = a
        self.h = a
        self.i = a

    def __repr__(self):
        return 'A(' + str(self.a) + ')'

    def __str__(self):
        return str(self.a)

    def __lt__(self, other):
        return self.a < other.a

    def __le__(self, other):
        return self.a <= other.a

    def __eq__(self, other):
        return self.a == other.a

    def __ne__(self, other):
        return self.a != other.a

    def __gt__(self, other):
        return self.a > other.a

    def __ge__(self, other):
        return self.a >= other.a

    def __cmp__(self, other):
        if self.a < other.a:
            return -1
        elif self.a > other.a:
            return 1
        else:
            return 0

def sizeof_As(As):
    numBytes = reduce(lambda acc,a: acc + sys.getsizeof(a), As, 0)
    return numBytes

def main():
    a1 = A(1)
    a2 = A(2)
    As = map(lambda x: A(x), range(0,10))
    sizes = map(lambda a: sys.getsizeof(a), As)
    print As
    print 'sizes = %r' % sizes
    print 'sizeof(As) = %d' % sizeof_As(As)

    print 'sizeof(a1) = %d' % sys.getsizeof(a1)
    

    print 'repr(a1) = %r' % a1
    print 'str(a1) = %s' % a2

    print 'a1 < a2 = %r' % (a1 < a2)
    print 'a1 <= a2 = %r' % (a1 <= a2)
    print 'a1 == a2 = %r' % (a1 == a2)
    print 'a1 != a2 = %r' % (a1 != a2)
    print 'a1 <> a2 = %r' % (a1 <> a2)
    print 'a1 > a2 = %r' % (a1 > a2)
    print 'a1 >= a2 = %r' % (a1 >= a2)

    b1 = eval(repr(a1))
    print 'b1.a = %s' % b1.a

    return

if __name__ == '__main__':
    main()
