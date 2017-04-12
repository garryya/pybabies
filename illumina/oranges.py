#!/usr/bin/python3 -B

#TODO docs
#TODO file doc
#TODO range - OrderedSet

"""
    oranges.py -
        command line tool ............



    Usage:
        post-review [-h] [--verbose] [--save-only] [--just-publish] [--latest] [--summary SUMMARY] [FILES]

"""

import os
import sys
import re
import logging
from optparse import OptionParser


LOG = logging.getLogger('oranges')


class Regions:

    def __init__(self, regions_file, bad_line_rate=80):
        """
        Reads and ......
        :param regions_file:
        :param bad_line_rate: bad lines percentage
        :return: True
        """
        self.regions_file = regions_file
        self.bad_line_rate = bad_line_rate
        self.loaded = self._load()

    def _load(self):
        self.regions = {}
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
                    r = (start, end)
                    self.regions[r] = 1
                except Exception as x:
                    LOG.warning('bad line: "{}" (exc:{})'.format(l, x))
        regions_loaded = len(self.regions)
        LOG.info('Lines read: {}'.format(lines_read))
        LOG.info('Regions loaded: {}'.format(regions_loaded))
        return regions_loaded >= (self.bad_line_rate/100)*lines_read


    def assign_rows(self, save_to_file=True):
        """
        :return:
        """
        LOG.debug('Assigning rows...')
        if not self.regions:
            LOG.error('Regions are empty')
            return False
        regs = sorted(self.regions.keys())
        for i0 in range(len(regs)):
            _, end0 = regs[i0]
            for rk in regs[i0+1:]:
                start, _ = rk
                if start >= end0:
                    break;
                self.regions[rk] += 1
        if save_to_file:
            outfile = os.path.splitext(self.regions_file)
            outfile = outfile[0] + '-stack-output' + outfile[1]
            LOG.debug('Saving to file {}...'.format(outfile))
            with open(outfile, 'w') as f:
                for r in regs:
                    f.write('{}\n'.format(self.regions[r]))
        return True

    def consolidate_ovelapping_regions(self, save_to_file=True):
        """
        :return:
        """
        LOG.debug('Consolidating rows...')
        if not self.regions:
            LOG.error('Regions are empty')
            return False
        if save_to_file:
            outfile = os.path.splitext(self.regions_file)
            outfile = outfile[0] + '-consolidated-output' + outfile[1]
            LOG.debug('Saving to file {}...'.format(outfile))
        return True

###

def set_logging(verbose=False, level=logging.DEBUG):
    fmt = '%(asctime)s - %(name)-6s - %(levelname)-6s - [%(filename)s:%(lineno)d] - %(message)s'
    logging.basicConfig(filename='oranges.log', level=level, format=(fmt))
    if verbose:
        h = logging.StreamHandler(sys.stdout)
        h.setFormatter(fmt=logging.Formatter(fmt))
        h.setLevel(level=level)
        LOG.addHandler(h)

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('--verbose', '-v', dest="verbose", action="store_true", default=False, help="verbose output")
    options, args = parser.parse_args()
    set_logging(verbose=options.verbose)
    regions_file = args[0] if args else ''
    LOG.info('args: %s | %s' % (options, regions_file))

    regions = Regions(regions_file)
    if not regions.loaded:
        LOG.error('Regions not loaded, exitting...')
        sys.exit(1)

    if not regions.assign_rows():
        sys.exit(1)

    if not regions.consolidate_ovelapping_regions():
        sys.exit(1)




    print()







