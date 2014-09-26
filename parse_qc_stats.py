import sys
import os
import re
import glob
import argparse
import subprocess
import pysam
import rmdup_calc
import AlignedStats
"""
Generate data accounting, and alignment stats on "
1) HGAC google doc - what they generated
2) Raw data directory - seq files copied from bionimbus
3) location of unaligned .bam files
4) location of aligned .bam files

"""

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
    print >>sys.stderr, "ERROR: unable to open " + flagstats_file + "for reading."
    return None

def count_seq_files(seq_dir):
  """
  Count number of paired-end seq files per library
  :returns: dict
  """
  d = dict()
  for seqfile in glob.glob(seq_dir + '/2*_[1-8]_[12]_sequence.txt.gz'):
    try:
      match = re.search(r'/(2\d+-\d+)_', seqfile)
      if match:
        filename = match.group(1)
        if filename in d:
          num_files = d[filename]
          d[filename] = num_files + 1
        else:
          d[filename] = 1
    except:
      sys.stderr.write('ERROR: didn\'t find any paired-end sequence.txt.gz files\n')
      d[filename]=0
  return d


def count_unaligned_readgroups(dir_path, seq_dict):
  """
  Count the readgroups from the unaligned .bams for each library
  :param dir_path: Path to dir containing unaligned sample directories
  :param seq_dict: dict of library ID's
  :returns: dict of readgroup counts by library
  """
  d = dict()
  for id in seq_dict:
    try:
      bam_file = dir_path + "/" + id + "/" + id + '.bam'
      bam = pysam.Samfile(bam_file, check_sq=False)
      d[id] = len(bam.header['RG']) * 2
    except:
      print >>sys.stderr, "problem with " + id + ": " + bam_file
      e = sys.exc_info()[0]
      print >>sys.stderr, e
      d[id] = 0
  return d 


def parse_unaligned_reads(dir_path, seq_dict):
  """
  grab the # of reads from the unaligned .bam.flagstats
  """
  d = dict()
  for id in seq_dict:
    try:
      flagstats_file = dir_path + "/" + id + "/" + id + '.bam.flagstats'
      fd = parse_flagstats(flagstats_file)
      d[id] = fd['total_reads']
    except:
      print >>sys.stderr, "problem parsing " + flagstats_file
      e = sys.exc_info()[0]
      print >>sys.stderr, e
      d[id] = 0
  return d


def parse_aligned_stats(rg_file_paths, seq_dict):
  aligned_d = dict()
  f = open(rg_file_paths, 'r')
  for file_path in f:
    file_path = file_path.strip()
    try:
      data_path, rg_file = os.path.split(file_path)
      id = os.path.split(data_path)[1]
      a_stats = AlignedStats.aligned_stats(id)
      a_stats.rg_file = file_path
      aligned_d[id] = a_stats
    except:
      print >>sys.stderr, "problem with " + id +": " + file_path
      e = sys.exc_info()[0]
      print >>sys.stderr, e
  return aligned_d


def compare_with_hgac(filename, seq_d, unaligned_d, unaligned_reads, aligned_d):
  """
  Parse HGAC record of files genearted per library
  Annotate with the other dicts
  print as results table
  """
  hgac = open(filename, 'r')
  print "BID\tHGAC_files\tBeagle_files\tUnaligned_files\tAligned_files\tRaw_reads\tContig_rmdup_pct\tReadgroup_rmdup_pct\ttotal_reads\tmapped\t%mapped\tDoC\t%_8x" # header
  for line in hgac:
    line = line.strip()
    try:
      id = line.split()[0]
      stats_string = ""
      a_stats = ''
      if id in aligned_d:
        a_stats = aligned_d[id]
      else:
        a_stats = AlignedStats.aligned_stats(id)

      print "%s\t%i\t%i\t%i\t%i\t%.4f\t%.4f\t%i\t%i\t%.2f\t%.2f\t%.2f" % (line,
          seq_d[id],
          unaligned_d[id],
          a_stats.number_of_files,
          unaligned_reads[id],
          a_stats.contig_rmdup_pct,
          a_stats.readgroup_rmdup_pct,
          a_stats.total_reads,
          a_stats.mapped_reads,
          a_stats.pct_mapped,
          a_stats.depth_of_coverage,
          a_stats.cov_8x)

    except IndexError:
      print line
    except:
      print "%s" % line
      e = sys.exc_info()
      sys.stderr.write(id + ' had no entry in at least one of the dicts: ' + str(e) + '\n')


def main():
  """
  parse command line args
  """
  p = argparse.ArgumentParser()
  p.add_argument('-r', dest='readgroups_file', action='store', required=True, 
      help='List of all RGfiles.txt file paths')
  p.add_argument('-H', dest='hgac_file', action='store', required=True, 
      help='HGAC sequence file counts by library')
  p.add_argument('-s', dest='seq_dir', action='store', required=True,
      help='Directory containing raw seq data files')
  p.add_argument('-u', dest='unaligned_dir', action='store', required=True,
      help='Directory containing unaligned bam files')

  args = p.parse_args()

  seq_dict = count_seq_files(args.seq_dir)
  aligned_dict = parse_aligned_stats(args.readgroups_file, seq_dict)
  unaligned_dict = count_unaligned_readgroups(args.unaligned_dir, seq_dict)
  unaligned_reads = parse_unaligned_reads(args.unaligned_dir, seq_dict)
  
  compare_with_hgac(args.hgac_file, seq_dict, unaligned_dict, unaligned_reads, aligned_dict)


if __name__ == '__main__':
  main()
