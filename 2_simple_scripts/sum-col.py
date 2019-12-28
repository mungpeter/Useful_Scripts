#!/usr/bin/python

##########

##########

import sys,numpy,glob,re,gzip,bz2
from CommonUtility import *

msg ="""
    Usage: > {0} [Filename] [Column no.]\n""".format(sys.argv[0])
if len(sys.argv) != 3: sys.exit(msg)

file_inp = glob.glob(sys.argv[1])[0]
col      = int(sys.argv[2])-1

file_handle = open(file_inp)
if re.search(r'.gz', file_inp):
  file_handle = gzip.open(file_inp, 'r')
elif re.search(r'.bz2', file_inp):
  file_handle = bz2.BZ2File(file_inp, 'r')
print("## Opening "+file_inp)

with file_handle as f:
  Data = []
  for line in f:
    if re.search(r'^#', line): continue
    if not line.strip(): continue
    Cell = line.split()
    if re.search(r'[a-zA-Z]',Cell[col]): continue
    print(str(Cell[col]))
    Data.append(float(Cell[col]))

sum   = numpy.sum(Data)
mean  = numpy.mean(Data)
media = numpy.median(Data)
stdev = numpy.std(Data)
max   = numpy.max(Data)
min   = numpy.min(Data)
print("\n%5s  %7s  %7s  %7s  %7s  %7s %7s" % ('No.', 'Sum', 'Mean', 'Stdev', 'Median', 'max', 'min'))
print("%5d  %7.3f  %7.5f  %7.5f  %7.5f  %7.5f  %7.5f\n" % (len(Data), sum, mean, stdev, media, max, min))
