import rethinkdb as r
from collections import defaultdict
import sys

class HgacRethinkdb:
  '''
  Provide functionality for querying the HGAC metadata 
  stored in rethinkDB
  __init__ creates the connection
  get_pair_columns returns dict of 2 queried columns
  '''

  def __init__(self, host, db, keyfile):
    '''
    Read keyfile and create connection
    '''
    self._host = host
    self._db = db
    self._keyfile = keyfile
    self._auth_key = self.__read_keyfile(self._keyfile)
    self._conn = self.__connect(host, self._auth_key)


  def __read_keyfile(self, keyfile):
    try:
      fh = open(keyfile, 'r')
      AUTH_KEY = fh.readline().strip()
      fh.close()
      return AUTH_KEY
    except IOError:
      print >>sys.stderr, "[HgacRethinkdb exception] - Unable to parse keyfile: " + keyfile
      sys.exit(1)


  def __connect(self, host, AUTH_KEY):
    return r.connect(host, auth_key=AUTH_KEY)


  def print_columns(self, table, cols):
    for record in r.db(self._db).table(table).pluck(cols).run(self._conn):
      print('\t'.join([str(x) for x in sorted(record.values())]))


  def get_columns(self, table, cols):
    return list(r.db(self._db).table(table).pluck(cols).run(self._conn))


