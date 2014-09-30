qc_stats
========

usage: parse_qc_stats.py [-h] -r READGROUPS_FILE -k KEYFILE -s SEQ_DIR -u
                         UNALIGNED_DIR

optional arguments:
  -h, --help          show this help message and exit
  -r READGROUPS_FILE  List of all RGfiles.txt file paths, used to locate
                      alignment stats per sample
  -k KEYFILE          RethinkDB keyfile required to query HGAC metadata
  -s SEQ_DIR          Directory containing all raw seq data files
  -u UNALIGNED_DIR    Directory containing per-sample directories with
                      unaligned bam files
