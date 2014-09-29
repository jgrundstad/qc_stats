import rethinkdb as r
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
    #try:
    fh = open(keyfile, 'r')
    AUTH_KEY = fh.readline().strip()
    fh.close()
    return AUTH_KEY
    #except:
    #  print >>sys.stderr, "[HgacRethinkdb exception] - Unable to parse keyfile: " + keyfile
    #  sys.exit(1)


  def __connect(self, host, AUTH_KEY):
    #try: 
    return r.connect(host, auth_key=AUTH_KEY)
    #except:
    #  print >>sys.stderr, "[HgacRethinkdb excpetion] - Unable to connect to host: " + host
    #  sys.exit(1)


  def print_columns(self, table, cols):
    for record in r.db(self._db).table(table).pluck(cols).run(self._conn):
      print('\t'.join([str(x) for x in record.values()]))


  def get_pair_columns(self, table, cols):
    d = dict()
    for record in r.db(self._db).table(table).pluck(cols).run(self._conn):
      if record.values()[1]:
        d[record.values()[0]] = record.values()[1]
      else:
        d[record.values()[0]] = '-'

    return d



