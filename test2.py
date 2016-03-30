#!/usr/bin/python
"""
"""
__author__ = 'garryya'
__version__     = '0.1'

import sys
from grutils import runcmd, runcmdo
import time
import threading

counter = 0

class oldC:
    _lock = threading.Lock()
    def __init__(self):
        self.n = 1
    def __str__(self):
        return self.__class__.__name__ + '::' + str(self.__dict__)
    def __enter__(self):
        self._lock.__enter__()
        #print self.__class__.__name__ + '::' + '__enter__'  + 'c=' + str(counter)
        print threading.currentThread().ident, '-->', str(counter)
        return self
    def __exit__(self, type, value, traceback):
        #print self.__class__.__name__ + '::' + '__exit__' + ' c=' + str(counter)
        print '\t', threading.currentThread().ident, '<--', str(counter)
        self._lock.__exit__()
        return self

class newC(oldC):
    def __init__(self, o):
        #self.__dict__ = o.__dict__
        self = o
    def __enter__(self):
        global counter
        counter += 1
        r = oldC.__enter__(self)
        return r
    def __exit__(self, type, value, traceback):
        global counter
        counter -= 1
        r = oldC.__exit__(self, type, value, traceback)
        return r

def getc(c):
    return newC(c)

def t1():
    oldc = oldC()
    with getc(oldc) as c:
        pass


####################

#threads = [threading.Thread(target=t1) for i in range(10)]
#[t.start() for t in threads]
#[t.join() for t in threads]

#t1()

class C:
    def dec(*required):
        def d_wrap(f):
            print '1 -> ', required
            def decorated(*args):
                print '2 -> ', args
                return f(*args)
            return decorated
        return d_wrap

    def argscheck(msg, *required):
        def d_required(f):
            def d(self, **kw):
                print 'required->', required
                print 'kw->', kw
                if required:
                    if not all((r in kw) for r in required):
                        return '%s (missing %s)' % (msg, ' or '.join(required))
                return f(self, **kw)
            return d
        return d_required


    @argscheck('JOPA', 'a')
    def func(self, **kw):
        return 'OK'




print C().func(**{'a':1,'b':2,'c':3})

