#!/usr/bin/python3

"""
    Fibonacci sequence (recursive+cache) - prints Nth number

    https://www.mathsisfun.com/numbers/fibonacci-sequence.html
"""

import sys

class fibonacci_cache(object):
    def __init__(self, f):
        self._func = f
        self._cache = {}
    def __call__(self, n, **kwargs):
        if n not in self._cache:
            self._cache[n] = self._func(n, kwargs)
        return self._cache[n]

@fibonacci_cache
def fibonacci(n, verbose=False):
    fn = n if n <= 1 else fibonacci(n-2, verbose=verbose) + fibonacci(n-1, verbose=verbose)
    if verbose:
        print('{} {}'.format(n, fn))
    return fn

if __name__ == '__main__':
    n = int(sys.argv[1])
    print('{}th fibonacci = {}'.format(n, fibonacci(n, verbose=True)))

