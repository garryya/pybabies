#!/usr/bin/python
""" Build Lowest Number by Removing n digits from a given number
    http://www.geeksforgeeks.org/build-lowest-number-by-removing-n-digits-from-a-given-number/

    Examples:

    Input: str = "4325043", n = 3
    Output: "2043"

    Input: str = "765028321", n = 5
    Output: "0221"

    Input: str = "121198", n = 2
    Output: "1118"

    (PYBABIES series)
"""
__author__ = 'GarryY'
__version__ = '1.0'

import sys


def seed_digits( s, ndigits, numbers_collector, number=''):
    if len(s)+len(number) < ndigits or ndigits <= 0:
        return

    for i in range(len(s)):
        nnumber = number+s[i]
        if len(nnumber) == ndigits:
            numbers_collector.append(nnumber)
        else:
            seed_digits(s[i+1:], ndigits, numbers_collector, nnumber)


##############  #################################

if len(sys.argv) < 3:
    print 'Arguments missing'
    sys.exit(1)

s = sys.argv[1]
n_digits_remove = int(sys.argv[2])
print 'Removing %s digits from <%s>' % (n_digits_remove, s)

numbers_collector = []
seed_digits(s, len(s)-n_digits_remove, numbers_collector)

for i in numbers_collector:
    print i

print 'Lowest number: ', sorted(numbers_collector)[0] if numbers_collector else '-'
