#!/usr/bin/python

import sys,re
#from CommonUtility import file_handle
import glob,gzip,bz2

msg = '''\n\t{0}\n\t\t[file]\n\t\t[separator]\n\t\t[column no. (can be mulitple)]\n\n\te.g.> x.py infile.txt ',' 2 3 5
\t\t[for tabs, type 'tab' without colons]'''.format(sys.argv[0])
if len(sys.argv) < 4: sys.exit(msg)

infile  = sys.argv[1]
delim   = sys.argv[2]
columns = sys.argv[3:]

def file_handle(file_name):
  if re.search(r'.gz$', file_name):
    handle = gzip.open(file_name, 'r')
  elif re.search(r'.bz2$', file_name):
    handle = bz2.BZ2File(file_name, 'r')
  else:
    handle = open(file_name, 'r')

#  print "## Opening "+file_name
  return handle



with file_handle(infile) as fi:
  if re.search(r'tab', delim):
    lines = [l.rstrip('\r|\n').split('\t') for l in fi]
  elif re.search(r' ', delim):
    lines = [l.rstrip('\r|\n').split() for l in fi]
  else:
    lines = [l.rstrip('\r|\n').split(delim) for l in fi]

for line in lines:
  for j in columns:
    try:
      print( line[int(j)-1] ),
      print('\t'),
    except IndexError:
      continue
  print('')


#  for i in range(len(columns)):
#    for j in columns:
#      try:
#        print( line[int(j)-1] ),
#        print(' '),
#      except IndexError:
#        continue
#  print('')
