#!/usr/bin/python2

"""
    Interview Cake
    https://www.interviewcake.com/all-questions
"""


import sys

def  StairCase(n):
    fmt = '{:>%d}' % n
    for i in range(1, n+1):
        print(fmt.format('#'*i))


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



# https://www.interviewcake.com/question/python/product-of-other-numbers
# You have a list of integers, and for each index you want to find the product of every integer except the integer at that index.
def get_products_except_index(ilist):
    istack = []
    for i in range(len(ilist)):
        istack.append(ilist[i])
        ilist[i] = ilist[i-1] * istack[-2] if i > 0 else 1
    p = 1
    for i in reversed(range(len(ilist)-1)):
        p *= istack.pop()
        ilist[i] *= p
    return ilist


# https://www.interviewcake.com/question/python/highest-product-of-3
def get_product(l):
    return reduce(lambda p, i: p*i, l, 1)

def highest_product_of_3__sorted1(ilist):
    ilist = sorted(ilist)
    neg2 = ilist[:2] if all([i<0 for i in ilist[:2]]) else []
    pos1 = ilist[-1:] if all([i>0 for i in ilist[-1:]]) else []
    pos3 = ilist[-3:] if all([i>0 for i in ilist[-3:]]) else []
    return max( get_product(neg2+pos1), get_product(pos3)) if (neg2 and pos1 or pos3) else None

def highest_product_of_3__sorted2(ilist):
    ilist = sorted(ilist)
    print('sorted: ', ilist)
    nneg = len([i for i in ilist if i<0])
    npos = len([i for i in ilist if i>0])
    if nneg >= 2 and npos >= 1:
        nprod = get_product(ilist[:2])*ilist[-1]
        #nprod = ilist[0]*ilist[1]*ilist[-1]
        return max(nprod, get_product(ilist[-3:])) if npos>=3 else nprod
    elif nneg >= 3 and npos <= 0:
        return get_product(ilist[-3:])
    else:
        return None


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
        return 0 #{(l,ls[l]) for l in ls}
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

    #ilist = [1, 7, 3, 4]
    #get_products_except_index(ilist)
    #print('CAKE: Get products except index: %s' % ilist)

    #ilist = [-10, -10, -1, -7, -3, 4]
    #ilist = [-10, -2, -1, -7, -3, 8, 9, 10, 4]
    ilist = [-10, -2, -1, -7, -3]
    p = highest_product_of_3__sorted2(ilist)
    print('Highest product of %s: %s' % (ilist, p))

    #FizzBuzz2()

    #most_common_substring2()
