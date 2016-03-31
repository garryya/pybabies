#!/usr/bin/python3

"""
    Interview Cake
    https://www.interviewcake.com/all-questions
"""


import sys

# 20m
def FizzBuzz1():
    #print('N = '),
    try:
        n = int(input())
    except:
        #print('ERR: integer expected')
        sys.exit(0)

    for i in range(1, n+1):
        fizz = not (i % 3)
        buzz = not (i % 5)
        if fizz and buzz:
            print('FizzBuzz')
        elif fizz:
            print('Fizz')
        elif buzz:
            print('Buzz')
        else:
            print(i)


# 20m
def FizzBuzz2():
    try:
        N = int(input())
        for i in range(1, N+1):
            fizz = not i % 3
            buzz = not i % 5
            print('{}{}{}'.format('Fizz' if fizz else '',
                                    'Buzz' if buzz else '',
                                    '' if fizz or buzz else str(i)))
    except Exception as e:
        print(e)







def get_products_except_index(ilist, verbose=False):
    if verbose:
        print('\toriginal: {}'.format(ilist))
    # calc and store the product 'before'
    llen = len(ilist)
    tlist = list(ilist)
    product = 1
    for i in range(llen):
        new_product = product * tlist[i]
        tlist[i] = product
        product = new_product
    if verbose:
        print('\thalf-product {}'.format(tlist))
    # finilizing
    rlist = list(ilist)
    for i in reversed(range(llen)):
        rlist[i] = tlist[i] * (ilist[i+1] if i < llen-1 else 1)
    return rlist


# http://stackoverflow.com/questions/14670632/algorithm-to-find-the-most-common-substrings-in-a-string
def most_common_substring2():
    try:
        N = int(input())
        K, L, M = (int(v) for v in input().split())
        S = input()[:N]
        submap = {}
        for i in range(len(S)):
            for l in range(K, L+1):
                if i+l > len(S):
                    continue
                s = S[i:i+l]
                # distinction check
                if len(set(s)) > M:
                    continue
                if s not in submap:
                    submap[s] = 0
                submap[s] += 1
        print(max([n for n in submap.values()]) if submap else 0)
    except Exception as e:
        print('bad input', str(e))


if __name__ == '__main__':

    ilist = [1, 7, 3, 4]
    #print('CAKE: Get products except index: {}'.format(get_products_except_index(ilist, verbose=True)))

    #FizzBuzz2()

    most_common_substring2()
