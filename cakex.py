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


# http://algorithms.tutorialhorizon.com/dynamic-programming-longest-common-substring/
# http://stackoverflow.com/questions/14670632/algorithm-to-find-the-most-common-substrings-in-a-string
# naive
def most_common_substring_data():
    try:
        """
        N = int(input())
        K, L, M = (int(v) for v in input().split())
        S = input()[:N]
        """
        N = 5
        K, L, M = 1, 5, 10
        S = 'ababc'
        ls = locals()
        return {l:ls[l] for l in ls}
    except Exception as e:
        print('bad input', str(e))
        sys.exit(1)

def most_common_substring1():
    data = most_common_substring_data()
    submap = {}
    for i in range(len(data['S'])):
        for l in range(data['K'], data['L'] + 1):
            if i + l > len(data['S']):
                continue
            s = data['S'][i:i + l]
            # distinction check
            if len(set(s)) > data['M']:
                continue
            if s not in submap:
                submap[s] = 0
            submap[s] += 1
    print(max([n for n in submap.values()]) if submap else 0)

# DP
def most_common_substring2():
    try:
        data = most_common_substring_data()
        s = data['S']
        srange = range(len(s))
        m = [[0 for _ in srange] for _ in srange]
        mij = (-1,-1)
        for i in srange:
            for j in srange[i:]:
                if i !=j and s[i] == s[j]:
                    m[i][j] = 1 + (m[i-1][j-1] if i>0 and j>0 else 0)
                    if mij == (-1,-1) or m[mij[0]][mij[1]] < m[i][j]:
                        mij = (i, j)
        #for r in m:
        #    print(r)
        if mij != (-1,-1):
            print('max common substring L={:d} -> {}'.format(m[mij[0]][mij[1]], mij))
    except Exception as e:
        print('bad input', str(e))


if __name__ == '__main__':

    ilist = [1, 7, 3, 4]
    #print('CAKE: Get products except index: {}'.format(get_products_except_index(ilist, verbose=True)))

    #FizzBuzz2()

    most_common_substring2()
