#!/usr/bin/python3 -B

'''
    File name: test.py
    Author: GarryY
    Date created: 4/12/2017
    Python Version: 3+

    oranges.py - a command line tool helping to draw genome regions and supporting the following modes:
        - stackup: ovelapped regions stack up and a row number is assigned
        - segmentify: consolidating regions into not overlapping segments

    The mode is selected using the options below (--stackup is default, --segmentify if both)
    The output is saved in file named REGIONS-FILE-output.txt, and content according to the requirements and a mode selected
    Debug log is saved in oranges.log file.


    Usage: oranges.py REGIONS-FILE [options]

    Options:
          -h, --help     show this help message and exit

          --stackup      stack up ovelapped regions (default)
          --segmentify   consolidate overlapping regions into segments

          --draw         draw region stacks

          -v, --verbose  verbose output
          -d, --debug    debug output

    Usage examples:

        ./oranges.py Regions_Small.txt --draw
            - run --stackup mode silently, draw and show stacked regions graph; saving result in Regions_Small-output.txt

        ./oranges.py Regions_Small.txt --segmentify --verbose
            - silently run --segmentify mode verbosely sending logs to both file and stdout; saving result in Regions_Small-output.txt

'''
import os
import sys
import re
import logging
from collections import namedtuple


LOG = logging.getLogger('oranges')


class Regions:

    def __init__(self, regions_file, bad_line_rate=80):
        self.regions_file = regions_file
        outfile = os.path.splitext(self.regions_file)
        self.outfile = outfile[0] + '-output' + outfile[1]
        self.bad_line_rate = bad_line_rate
        self.clusters = []
        self.loaded = self._load()

    def _load(self):
        """
        Reads and verifies region data
        :return: True if read count is greater than bad_line_rate% of total line
        """
        self.regions = []
        if not self.regions_file:
            LOG.error('Regions file not specified')
            return False
        if not os.path.exists(self.regions_file):
            LOG.error('Regions file does not exists: {}'.format(regions_file))
            return False
        lines_read = 0
        with open(regions_file) as rf:
            for l in rf.readlines():
                lines_read +=1
                try:
                    start, end = (int(v) for v in re.split(r'\s', l.strip()))
                    r = [start, end, 1]
                    self.regions.append(r)
                except Exception as x:
                    LOG.warning('bad line: "{}" (exc:{})'.format(l, x))
        regions_loaded = len(self.regions)
        LOG.info('Lines read: {}'.format(lines_read))
        LOG.info('Regions loaded: {}'.format(regions_loaded))
        return regions_loaded >= (self.bad_line_rate/100)*lines_read


    def stackup_regions(self, save_to_file=True, debug=False, save_sorted=False):
        """
        Algorithm idea : collect all 'chained' regions into clusters;
        a stacked region row is initially 1 and calculated as contiguos overlapped region chain length

                3 ----
            2 ------   2 ---
        1 -----------------    1 ----

        complexity: O(n**2)

        """
        LOG.debug('Stacking up regions and assigning rows...')
        if not self.regions:
            LOG.error('Regions are empty')
            return False
        self.clusters = []
        cluster = []
        regs = sorted(self.regions)
        for i0 in range(len(regs)):
            r0 = regs[i0]
            _, end0, row0 = r0
            is_last = r0 == regs[-1]
            if cluster and (row0==1 or is_last):
                self.clusters.append(cluster)
                if not is_last:
                    cluster = []
            cluster += [r0]
            for r in regs[i0+1:]:
                start, _, row = r
                if start >= end0:
                    break;
                r[2] = row + 1
        if save_to_file:
            LOG.debug('Saving to file {} ...'.format(self.outfile))
            with open(self.outfile, 'w') as f:
                regs = regs if save_sorted else self.regions
                for r in regs:
                    s = r[2] if not debug else ' '.join(str(v) for v in r)
                    f.write('{}\n'.format(s))
        return True

    def segmentify_regions(self, save_to_file=True):
        """
        Algorithm idea : for each cluster from clusters collected by stackup-stage list and sort all regions
        edges:
        [[s1, row1], [s2, row2], [s3, row3], [e2, -row2], .... ]
        (negative row indicates that the boundary is a region end)

                3 s3-----e3
            2 s2------e2     2 s4---e4
        1 s1---------------------------e1

          s1--s2--s3--e2-e3----s4---e4-e1

        Each adjacent pair of edges defines a segment: [[s1, s2-1, count], [s2, s3-1, count].... ]
        count is edge row if start, or abs(row)-1

        complexity: O(n**2)

        """
        LOG.debug('Consolidating ovelapping regions...')
        if not self.clusters:
            LOG.error('Clusters are empty: stackup stage ismissing ')
            return False

        segments =[]
        for c in self.clusters:
            edges =[]
            for reg in c:
                s, e, row = reg
                edges += [[s, row], [e, -row]]
            edges = sorted(edges, key=lambda v: v[0])
            for i in range(len(edges)-1):
                e1 = edges[i]
                e2 = edges[i+1]
                s = e1[0]
                e = e2[0] if e2 == edges[-1] else e2[0]-1
                count = abs(e1[1])
                if e1[1] < -1:
                    count -= 1
                seg = [s, e, count]
                segments.append(seg)

        if save_to_file:
            LOG.debug('Saving to file {} ...'.format(self.outfile))
        with open(self.outfile, 'w') as f:
            for s, e, count in segments:
                f.write('{} {} {}\n'.format(s, e, count))
        return True

    def draw_stacks(self):
        LOG.debug('Drawing ...')
        try:
            import numpy as np
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.margins(0.1)
            for s, e, r in self.regions:
                plt.plot([s, e if e>s else e+100], [r, r], label='{} {}-{}'.format(r, s, e), lw=5)
            plt.show()
        except ImportError as x:
            LOG.warning('Cannot draw: {}'.format(x))


#############################


def set_logging(verbose=False, level=logging.DEBUG):
    fmt = '%(asctime)s - %(name)-6s - %(levelname)-6s - [%(filename)s:%(lineno)d] - %(message)s'
    logging.basicConfig(filename='oranges.log', level=level, format=(fmt))
    h = logging.StreamHandler(sys.stdout)
    h.setFormatter(fmt=logging.Formatter('%(levelname)-6s - %(message)s'))
    h.setLevel(level=logging.WARNING if not verbose else logging.DEBUG)
    LOG.addHandler(h)


def parse_options():
    try:
        from optparse import OptionParser
        usage = 'usage: %prog REGIONS-FILE [options]'
        parser = OptionParser(usage=usage)
        parser.add_option('--stackup', dest="stackup", action="store_true", default=True, help="stack up ovelapped regions (default)")
        parser.add_option('--segmentify', dest="segmentify", action="store_true", default=False, help="consolidate overlapping regions into segments")
        parser.add_option('--verbose', '-v', dest="verbose", action="store_true", default=False, help="verbose output")
        parser.add_option('--debug', '-d', dest="debug", action="store_true", default=False, help="debug output")
        parser.add_option('--draw', dest="draw", action="store_true", default=False, help="draw_stacks regions")
        options, args = parser.parse_args()
    except ImportError:
        args = sys.argv[1:]
        Options = namedtuple('Options', ['stackup', 'segmentify', 'verbose', 'debug', 'draw'])
        options = Options(stackup='--stackup' in args,
                          segmentify='--segmentify' in args,
                          verbose='--debug' in args,
                          debug='--debug' in args,
                          draw='--draw' in args)
    return options, args


if __name__ == '__main__':
    options, args = parse_options()
    set_logging(verbose=options.verbose)
    regions_file = args[0] if args else ''
    LOG.info('args: %s | %s' % (options, regions_file))

    if options.stackup and options.segmentify:
        options.stackup = False

    regions = Regions(regions_file)
    if not regions.loaded:
        LOG.error('Regions not loaded, exitting...')
        sys.exit(1)

    if options.stackup:
        if not regions.stackup_regions(debug=options.debug, save_to_file=True, save_sorted=False):
            sys.exit(1)
        if options.draw:
            regions.draw_stacks()
    elif options.segmentify:
        if not regions.stackup_regions(debug=options.debug, save_to_file=False, save_sorted=False):
            sys.exit(1)
        if not regions.segmentify_regions():
            sys.exit(1)

    print('Done')






