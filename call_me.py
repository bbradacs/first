# test syntax for calling a function with a variable number of arguments

def call_me(proc, *args):
    retval = proc(*args)
    return retval

def one_arg(arg):
    print 'one_arg(' + repr(arg) + ')'
    return arg

def two_args(arg1, arg2):
    print 'two_args(' + repr(arg1) + ',' + repr(arg2) + ')'
    return 2

def three_args(arg1, arg2, arg3):
    print 'three_args(' + repr(arg1) + ',' + repr(arg2) + ',' + repr(arg3) + ')'
    return 'three'


def main():
    r1 = call_me(one_arg, 'first arg')
    r2 = call_me(two_args, 1, 'four')
    r3 = call_me(three_args, 1, 2, 3)

    print 'r1 = ' + repr(r1)
    print 'r2 = ' + repr(r2)
    print 'r3 = ' + repr(r3)

    return

if __name__ == '__main__':
    main()


