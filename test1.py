#!/grid/common/pkgs/python/v3.4.0/bin/python3.4 -B
"""
"""
__author__ = 'garryya'
__version__     = '0.1'

import sys
import os
import re
import time
import logging
from optparse import OptionParser, OptionGroup
import argparse
import traceback
from collections import OrderedDict, namedtuple
import json
from twisted.internet import reactor, error, defer
from twisted.internet.threads import deferToThread
from grutils import DeferredLockSet, handle_exception, kill_process, get_fqdn, time2epoch, setup_logging, time2str
from grutils import get_pid_by_namepath, is_process_running, check_long_option_typo
from threading import Lock, Thread
import lxml.html as LH
from copy import deepcopy
from flask import Flask, render_template
import tempfile

#print sys.argv[1:]


def  StairCase(n):
    fmt = '{:>%d}' % n
    for i in range(1, n+1):
        print(fmt.format('#'*i))
#StairCase(int(sys.argv[1]))

def _finally():
    try:
        raise KeyError
        #a = int('aaaaa')
        print(1)
        #os.exit(0)
    except Exception as e:
        print('EXC!!')
    finally:
        print('finally')

def is_valid_time(option, opt_str, value, parser):
    parser.values.T = time2epoch(value)


def test_optparser():
    parser = OptionParser()
    g1 = OptionGroup(parser, 'G1')
    g2 = OptionGroup(parser, 'G2')
    parser.add_option("-a", "--action", dest='action', action='store_true', default=False, help="aaaaaa what to do")
    parser.add_option("--jopa", dest='jopa', action='store_true', default=False, help="aaaaaa what to do")
    g1.add_option("--l1", dest='l1', action='store_true', default='l1', help="l1")
    g1.add_option("-b", dest='bb', action='store_true', default='bb', help="bb")
    g2.add_option("--l2", dest='l2', action='store_true', default='l2', help="l2")
    # g2.add_option('--start-time',
    #               dest='T',
    #               action='callback',
    #               # callback=is_valid_time,
    #               type = str,
    #               default=time2epoch(),
    #               help="TIME")
    opt_wrong, opt_implied = check_long_option_typo(parser, sys.argv[1:])
    if opt_wrong:
        print('probably wrong option {}: do you mean {}'.format(opt_wrong, opt_implied))
        sys.exit(1)
    parser.add_option_group(g1)
    parser.add_option_group(g2)
    opts, args = parser.parse_args()
    print(opts, args)


def fff():
    print('STACK:\n')
    tb = traceback.format_stack()[:-1]
    #print(tb)
    #print('XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX')
    print(''.join(tb))


def test_argparser():
    parser = argparse.ArgumentParser()
    g = parser.add_mutually_exclusive_group()
    #parser.add_argument("-a", "--action", dest='action', action='store_true', default='a', metavar=argparse.SUPPRESS)
    # parser.add_argument("-b", dest='bb', action='store_true', default='bb', help="bb")
    # g.add_argument("--l1", dest='l1', action='store_true', default='l1', help="l1")
    # g.add_argument("--l2", dest='l2', action='store_true', default='l2', help="l2")
    # opts, args = parser.parse_args()
    # print(opts, args)
    fff()


def dec(o):
    from grutils import decob
    #print('{:_>16!s} --> {:_<!s}'.format(o, decob(o)))
    o_ = decob(o)
    print('{!s} --> {} {!s}'.format(o, type(o_), o_))


def test_dec():
    dec('abc')
    dec(b'abc')
    dec({b'a':1234, b'b':b'b', 'c':[1, 2, b'aaa', {1:1, 2:'2', 3:b'3', '3':b'3', b'4':b'4'}]})
    dec([b'abc', '123', b'456'])
    dec(set([b'abc', '123', b'456']))
    dec((b'abc', '123', b'456'))


def tb(e):
    tb = traceback.format_exception(type(e), e)
    print(tb)


def test_andy():
    inpfile = sys.argv[1]
    html = open('template.html').read()
    s = ''
    with open(inpfile) as f:
        for l in f.readlines():
            s += '<h2>{}</h2>\n'.format(l)
    html = html.replace('%%NETS%%', s)
    with open(inpfile+'.html','w') as f:
        f.write(html)





#############################################
#############################################


class Status:
    __status__ = True
    def __init__(self, name, id, text=None):
        self.id = id
        self.name = name
        self.text = text
    def __str__(self):
        return self.text
    def __repr__(self):
        return '({}): {}'.format(self.id, self.text)
    def format(self, add=None):
        return '{!r}{}'.format(self, '\n{}'.format(add) if add else '')
    def success(self):
        return self.id == 0

class StatusMap:
    def __init__(self, **status_list):
        for s, sv in status_list.items():
            if not isinstance(sv, tuple):
                sv = (sv, s)
            setattr(self, s, Status(s, *sv))
    def enumerate(self):
        return [getattr(self, a) for a in dir(self) if hasattr(getattr(self, a), '__status__')]
    def __str__(self):
        return '\n'.join([str(s) for s in self.enumerate()])


def test_status():
    ss = StatusMap(
        S1=1,
        S2=2,
        S3=(3,'SSS#3'),
    )

    print(ss)
    print('{0!r}'.format(ss.S1))
    print('{}'.format(ss.S1.format()))


def test_meta():
    JobSubproc_ = namedtuple('JobSubproc_', ['id', 'killf', 'verbose'])

    class JobSubproc(JobSubproc_):
        def __init__(self, id, killf, verbose):
            JobSubproc_.__init__(id, killf, verbose)
            self.kill = self.kill
        def __new__(cls, id, killf, verbose):
            return JobSubproc_.__new__(JobSubproc_, id, killf, verbose)
        def kill(self):
            return self.killf(self.id, verbose=self.verbose)

    class OSJobSubproc(JobSubproc):
        def __init__(self, pid, verbose=True):
            JobSubproc.__init__(id=pid, killf=kill_process, verbose=verbose)
        def __new__(cls, pid, verbose=True):
            return JobSubproc.__new__(cls, id=pid, killf=kill_process, verbose=verbose)

    class DRMJobSubproc(JobSubproc):
        def __init__(self, job_id, drm_obj, verbose=True):
            JobSubproc.__init__(id=job_id, killf=drm_obj.kill, verbose=verbose)
        def __new__(cls, job_id, drm_obj, verbose=True):
            return JobSubproc.__new__(cls, id=job_id, killf=drm_obj.kill, verbose=verbose)

    _JobSubprocSet = namedtuple('JobSubprocSet', ['os', 'drm'])
    JobSubprocSet = _JobSubprocSet(os=OSJobSubproc, drm=DRMJobSubproc)

    j1 = OSJobSubproc(-1)
    print(j1)
    j2 = DRMJobSubproc(-1, os)
    print(j2)

    # j1.kill()
    j2.kill()



from functools import wraps

def decor(dec_arg):
    def w(f):
        @wraps(f)
        def ww(*args, **dargs):
            dargs['add1'] = 'AAD1'
            dargs['DECARG'] = dec_arg
            return f(*args, **dargs)
        return ww
    return w

@decor('DECARG111')
def test_decorator(*args, **dargs):
    print('F({}, {})'.format(args, dargs))

#######################

# TODO !HACK ALERT! for long options with quoted string with spaces: --opt="a b    c" --> --opt="a,b,c"
def _hack_optparse_string_args(*argnames):
    hacked = []
    for a in argnames:
        print('XXX \t{}'.format(a))
        try:
            a = [o for o in argv if a in o][0]
            opt = a.split('=')
            print('XXX \t\t{}'.format(opt))
            if len(opt) == 2:
                val = opt[1].strip().strip('"').strip()
                val = re.sub(r'[,\+]*\s+[,\+]*', r',', val)
                hacked.append('{}="{}"'.format(opt[0], val))
                print('XXX \t\t\t{}'.format(hacked))
                argv.remove(a)
        except:
            pass
    for a in hacked:
        argv.append(a)


#print('XXX {}'.format(argv))
#_hack_optparse_string_args('--jobs')
#print('XXX {}'.format(argv))
###

def test_pid():
    name = sys.argv[1]
    path = sys.argv[2] # '/grid/cva/tools/js/2.0/dev/agents/sw-scd1'
    pids = get_pid_by_namepath(name, path, verbose=True)
    print('PIDs = {}'.format(pids))


def test_pid_is_running():
    for pid in sys.argv[1:]:
        running = is_process_running(pid, nchecks=1)
        print('PID = {} is {} running'.format(pid, '' if running else 'not'))

def list_dirfiles(e):
    dirfiles = []
    # for b in e.iterdescendants(tag='b'):
    for e in e.iterchildren():
        if e.tag != 'b':
            continue
        text = e.text_content()
        if text and re.match(r'^[\w\-\.]+$', text):
            dirfiles.append(text)
    return dirfiles



def is_filename(text, pattern=r'^[\w\-]+\.[hHcC]p{0,2}$'):
    return re.match(pattern, text)

def parse_paths(hul, path, paths):
    for e in hul.iterchildren():
        if e.tag != 'ul':
            continue
        for df in list_dirfiles(e):
            text = df.text_content()
            if is_filename(text):
                path_str = '/'.join(path)
                paths[path_str] = []
                for err in df.iterchildren('ul'):
                    paths[path_str].append(err)
            elif text:
                path_copy = deepcopy(path) + [text]
                parse_paths(df, path_copy, paths)
            else:
                # TODO log....
                continue

def _location(ul):
    lis = list(ul.itersiblings(tag='li', preceding=True))
    if lis:
        for b in lis[0].iterchildren('b'):
            loc = re.findall(r'[a-zA-Z_][\w\-\.]+', b.text_content())
            if loc:
                return loc[0]
    return ''



def walk_html(h, indent=0):
    papa = '{}:{}'.format(h.tag, _location(h))
    i = '\t' * indent
    l = list(h.iterchildren(tag='ul'))
    print('{}# {} #'.format(i, ','.join('{}-{}'.format(e.tag,_location(e)) for e in l)))
    for e in l:
        loc = _location(e)
        print('{}<{}> {} ||| {}'.format(i, e.tag, loc, papa))
        walk_html(e, indent=indent+1)

def _collect_kids(e, tag, tags):
    for t in e.iterchildren():
        if t.tag == tag:
            tags.append(t)
        _collect_kids(t, tag, tags)


def walk_errors(h, path, paths, loc=None):
    if loc and is_filename(loc):
        k = '/'.join(path)
        paths[k] = dict(h=h, errors={})
        errors = []
        _collect_kids(h, 'tr', errors)
        for err in errors:
            err_info = dict(description='?', rule='?')
            err_fields = list(err.iterchildren(tag='td'))
            assert len(err_fields) == 4
            descr = re.match(r'^(\d+)\:\s*(.*)$', err_fields[1].text_content(), re.M|re.DOTALL)
            if descr and len(descr.groups()) == 2:
                line = descr.groups()[0]
                err_info['description'] = descr.groups()[1].strip()
                err_info['rule'] = err_fields[3].text_content()
                err_info['.html2replace'] = LH.tostring(err_fields[1])
                print('{}{} : {}\n'.format('\t'*(len(path)+1), line, err_info))
                paths[k]['errors'][line] = err_info
        print('{} {} error(s) : {}'.format('\t' * len(path), len(paths[k]['errors']), k))
    else:
        for e in h.iterchildren(tag='ul'):
            loc = _location(e)
            new_path = deepcopy(path)
            if loc:
                new_path += [loc]
            print('{}<{}> {}'.format('\t' * len(path), e.tag, loc))
            walk_errors(e, new_path, paths, loc=loc)
    return True


def parse_report(report_html, modules):
    anchors = [r'findings by file',
               r'active rules']
    anchors_pos = {a:re.search(a, report_html, re.I) for a in anchors}
    if not all(p for p in anchors_pos.values()):
        print('Failed: one of the anchors not found ({})'.format(anchors_pos))
        sys.exit(1)

    report_html = report_html[anchors_pos[anchors[0]].start():anchors_pos[anchors[1]].start()]
    anchor1_corrected = r'<b>Total\s*[^\s<>]*</b></li>'
    anchor1_corrected_pos = re.search(anchor1_corrected, report_html, re.I)
    if not anchor1_corrected_pos:
        print('Failed: corrected anchors not found ({})'.format(anchor1_corrected))
        sys.exit(1)

    report_html = report_html[anchor1_corrected_pos.start()+len(anchor1_corrected):]

    h = LH.fromstring(report_html)

    path = []
    paths = {}
    walk_errors(h, path, paths)


def test_html_parsing():
    htmlf = '/home/garryya/rd/tmp/report.html.sav'
    # htmlf = '/home/garryya/rd/tmp/report.html'
    parse_report(open(htmlf).read(), None)


app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


def test_log():
    LOG = setup_logging('test1', logfile='test1.log', level=logging.DEBUG)


def test_stdin():
    while True:
        print('* waiting for input...')
        data = sys.stdin.readline()
        print('\t{} got: {}'.format(time2str(), data))

def test_pipe():
    tmpdir = '/tmp' # tempfile.mkdtemp()
    pname = 'test1pipe'
    ppath = os.path.join(tmpdir, pname)
    print('PID={} pipe={}'.format(os.getpid(), ppath))
    try:
        os.mkfifo(ppath)
    except OSError as x:
        print(x)
        sys.exit(1)
    with open(ppath, buffering=1) as p:
        while True:
            print('* waiting for input...')
            # data = sys.stdin.read()
            data = p.read()
            print('\t{} got: {}'.format(time2str(), data))

def test_pipe_tw():
    reactor.callLater(0, test_stdin)
    reactor.run()


def test_lock(l, s):
    print('{} enters'.format(s))
    if l.acquire(blocking=False):
        try:
            print('{} acquired'.format(s))
            time.sleep(3)
        finally:
            print('{} released'.format(s))
    else:
        print('{} denied'.format(s))


def test_lock_denied():
    lock = Lock()
    ss = ['A', 'B']
    threads = [Thread(target=test_lock, args=(lock, s), name=s) for s in ss]
    [t.start() for t in threads]
    [t.join() for t in threads]



try:

    print(sys.executable)
    print(sys.argv)

    print(os.path.dirname(os.path.realpath(__file__)))

    print(get_fqdn())

    #test_argparser()

    # test_optparser()

    # _finally()

    # test_meta()

    # test_cast()

    # test_decorator(1, 2, 3, 'QUQU', sss='SS')

    #print(rrun('cva-xeon114', 'garryya', 'Ptah12587', 'sudo ls', verbose=True))
    #print(rrun('hsv-scd107', 'root', 'cadence', 'ls', verbose=True))


    # test_pid()
    # test_pid_is_running()


    # test_html_parsing()


    # test_log()


    #test_pipe()


    # test_pipe_tw()

    test_lock_denied()

    pass

except KeyboardInterrupt:
    pass
except Exception as x:
    handle_exception(None, x, stack=True)