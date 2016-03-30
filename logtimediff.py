#!/grid/common/pkgs/python/v3.2.2/bin/python3.2
"""
"""
__author__ = 'garryya'
__version__     = '0.1'

import sys
from grutils import runcmd, runcmdo
from datetime import datetime as dt, timedelta as td

if len(sys.argv) <= 1:
    print('no file')
    sys.exit(1)

no_strict = False
if len(sys.argv) >= 3:
    no_strict = sys.argv[2] == '-nostrict'

#times = runcmdo('grep "TEST_ET.*EP:.*ES.*CSW:.*MSK:.*" %s | cut -d " " -f 4 | cut -d "-" -f 1' % sys.argv[1])
records = runcmdo('grep "TEST_ET.*EP:.*ES.*CSW:.*MSK:.*" %s' % sys.argv[1])

logfile = 'logtimediff.log'

res = []
with open(logfile,'w') as f:

    f.write(records)

    rr_prev = None
    for rr in records.split('\n'):
        r = rr.split()
        if rr_prev:
            r_prev = rr_prev.split()

            i1 = int(r_prev[4][:-1])
            i2 = int(r[4][:-1])
            j1 = int(r_prev[5])
            j2 = int(r[5])

            t1 = r_prev[3].split('-')[0]
            t2 = r[3].split('-')[0]
            tt1 = dt.strptime(t1,"%H:%M:%S:%f")
            tt2 = dt.strptime(t2,"%H:%M:%S:%f")
            delta = tt2 - tt1
            #if delta.seconds >= 1 and delta > td(0) and i1+1 == i2:
            #    res.append('%s|%s' % (t1,t2))
            if delta.seconds >= 1 and delta > td(0) and (no_strict or i1==i2 and j1+1 == j2):
                res.append('%s\n%s' % (rr_prev,rr))
        rr_prev = rr

    print(runcmdo('wc -l %s'%logfile))

    if res:
        print('\n',*res, sep='\n---\n', file=f)
        print(*res, sep='\n---\n')
        sys.exit(1)