import sys
import os
import glob
import argparse



def markDuplicates_pct(URD, RPD, URE, RPE):
  return float((URD + RPD * 2.0) / (URE + RPE * 2.0))


def combine(files):
  UNPAIRED_READ_DUPLICATES = 0 # URD
  READ_PAIR_DUPLICATES = 0     # RPD
  UNPAIRED_READS_EXAMINED = 0  # URE
  READ_PAIRS_EXAMINED = 0      # RPE
  for file in files:
    f = open(file, 'r')
    for i, line in enumerate(f):
      if i==7:
        toks = line.split()
      if i > 7:
        break

    f.close()
    UNPAIRED_READ_DUPLICATES = UNPAIRED_READ_DUPLICATES + int(toks[4])
    READ_PAIR_DUPLICATES = READ_PAIR_DUPLICATES + int(toks[5])
    UNPAIRED_READS_EXAMINED = UNPAIRED_READS_EXAMINED + int(toks[1])
    READ_PAIRS_EXAMINED = READ_PAIRS_EXAMINED + int(toks[2])

  PCT = markDuplicates_pct(UNPAIRED_READ_DUPLICATES, READ_PAIR_DUPLICATES, UNPAIRED_READS_EXAMINED, READ_PAIRS_EXAMINED)
  return PCT

def main():
  p = argparse.ArgumentParser(description='Combine Picard MarkDuplicates metrics for multiple files')
  p.add_argument('files', metavar='metrics_file', type=str, nargs='+',
      help='List of Picard Mark Duplicates metrics files')
  args = p.parse_args()
  pct = combine(args.files)
  print pct

if __name__ == '__main__':
  main()
