import rethinkdb as r
import sys
import argparse
from StringIO import StringIO

class HgacRethinkdb:
  

  def __init__(self, host, db, keyfile):
    self._host = host
    self._db = db
    self._keyfile = keyfile
    self._auth_key = read_keyfile(self._keyfile)
    self._conn = connect(host, self._auth_key)


  def read_keyfile(self, keyfile):
    fh = open(keyfile, 'r')
    AUTH_KEY = fh.readline().strip()
    fh.close()
    return AUTH_KEY

  def connect(self, host, AUTH_KEY):
    return r.connect(host, auth_key=AUTH_KEY)

  #def print_columns(db, table, conn, cols):
  #  for record in r.db(db).table(table).pluck(cols).run(conn):
  #    print('\t'.join([str(x) for x in record.values()]))

  def print_columns(self, table, cols):
    for record in r.db(self._db).table(table).pluck(cols).run(self._conn):
      print('\t'.join([str(x) for x in record.values()]))

'''
def main():

  parser = argparse.ArgumentParser(description='query FO_NBCP Library Tracker Google Doc')
  parser.add_argument('--keyfile', '-k', dest='keyfile', action='store', required=True, help='Auth_key file')
  args = parser.parse_args()
  
  AUTH_KEY = read_keyfile(args.keyfile)
  db = 'hgac'
  table = 'FONBC_LibraryTracker'
  file_column = 'Total # of Sequence Files from PE runs (AD)'

  conn = connect('igsbimg.uchicago.edu', AUTH_KEY)

  print_columns(db, table, conn, ['BID', file_column])
 

if __name__ == '__main__':
  main()
'''
