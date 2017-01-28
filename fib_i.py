#!/usr/bin/python3

"""
    Fibonacci sequence (iterative, bottom-up) - prints Nth number

    https://www.mathsisfun.com/numbers/fibonacci-sequence.html
"""

import sys

def fibonacci(n, verbose=False):
    assert n >= 0
    for i in range(n+1):
        fn = prev_prev + prev if i > 1 else i
        prev_prev = prev if i > 0 else 0
        prev = fn
        if verbose:
            print('{} {}'.format(i, fn))
    return fn

if __name__ == '__main__':
    n = int(sys.argv[1])
    print('{}th fibonacci = {}'.format(n, fibonacci(n, verbose=True)))
