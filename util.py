import os
import sys

GENOME_SIZE = 3101804739

def rl(fh, i):
  return fh.readline().split(' ')[i]

def parse_flagstats(flagstats_file):
  d = dict()
  try:
    fh = open(flagstats_file, 'r')
    '''
    895854478 + 0 in total (QC-passed reads + QC-failed reads)
    0 + 0 duplicates
    0 + 0 mapped (0.00%:-nan%)
    895854478 + 0 paired in sequencing
    447927239 + 0 read1
    447927239 + 0 read2
    0 + 0 properly paired (0.00%:-nan%)
    0 + 0 with itself and mate mapped
    0 + 0 singletons (0.00%:-nan%)
    0 + 0 with mate mapped to a different chr
    0 + 0 with mate mapped to a different chr (mapQ>=5)
    '''
    d['total_reads'] = int(rl(fh, 0))
    d['duplicates'] = int(rl(fh, 0))
    line = fh.readline()
    d['mapped_reads'] = int(line.split(' ')[0])
    d['pct_mapped'] = float(line.split(' ')[4].split(r'(')[1].split(r'%')[0])
    d['paired'] = int(rl(fh, 0))
    d['read1'] = int(rl(fh, 0))
    d['read2'] = int(rl(fh, 0))
    return d
  except IOError:
    print >>sys.stderr, "ERROR: unable to open for reading: " + flagstats_file
    return d


