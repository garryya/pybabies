#!/grid/common/pkgs/python/v3.4.0/bin/python3 -b

import sys
import random
import time

factor = 1.0
try:
	factor = float(sys.argv[1])
except:
	pass

days = {
    '1.MON': (7000,9000),
    '2.TUE': (7000,10000),
    '3.WED': (8000,10000),
    '4.THU': (7000,9000),
    '5.FRI': (7000,9000),
    '6.SAT': (14000,21000),
    '7.SUN': (14000,21000),
}


random.seed(time.time())

for w in ['week1','week2']:
    print(w)
    for d in sorted(days):
        dr = tuple([v*factor for v in days[d]])
        print('\t{} : {}'.format(d, random.randrange(*dr)))
