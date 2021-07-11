#!/usr/bin/env python3

import sys

msg = '''\n  > {0}
    [ list of completed jobs ]
    [ job number splitter ] 
    [ job number position (natural reading) ]
    [ total number of completed jobs there should be ]
    [ string with "XREPLACE" for list of imcomplete jobs]\n
  Job Number: e.g. zld20_wait.\033[33m12\033[0m/zld20_wait.\033[33m12\033[0m.sdf
              split by \033[32m'.'\033[0m, ['zld20_wait','12/zld20_wait',\033[33m'12'\033[0m,sdf']
              position \033[32m'3'\033[0m = \033[33m'12'\033[0m
 e.g.> x.py pass.list '.' 3 zld20_wait.XREPLACEX.smi.gz\n'''.format(sys.argv[0])
if len(sys.argv) != 6: sys.exit(msg)

import re
import pandas as pd

##########################################################################
def main():
  get_num = GetNum(idf=sys.argv[2], posit=int(sys.argv[3])-1)
  pr_name = PrintMissing(line=sys.argv[5])

  ## Read in rows of name, get the subset number and reorder it
  df = pd.read_csv(sys.argv[1], header=None, sep='\s+', names=['name'])
  df['num'] = df.name.apply(get_num)
  df.sort_values(by='num', ascending=True, inplace=True)
  df.reset_index(inplace=True)
  df.drop(['index'], axis=1, inplace=True)
  df.reset_index(inplace=True)

  ## Reference list: how many row numbers there should be
  tlist = [x for x in range(int(sys.argv[4]))]
  xdf = pd.DataFrame(tlist, columns=['num'])

  ## merge the input list to reference list to find which rows are missing
  cdf = pd.merge(xdf, df, on=['num'], how='left')

  ## find rows that have null value
  fdf = cdf[cdf.name.isnull()]
  fdf.num.apply(pr_name)


##########################################################################
## Get job number in the line
class GetNum(object):
  def __init__( self, idf='.', posit=None ):
    self.idf   = idf
    self.posit = posit
  def __call__( self, name ):
    return int(name.split(self.idf)[self.posit]) - 1

## print out missing job name
class PrintMissing(object):
  def __init__( self, line='' ):
    self.line = line
  def __call__( self, num ):
    print(re.sub('XREPLACEX', str(num+1) , self.line ))


##########################################################################
if __name__ == '__main__':
  main( )

#######################################################################
#
#  Peter M.U. Ung @ gRED
#
#  v1   20.07.19
#
#  check the completion of jobs with numbers in filename
#    e.g. zld20.12/zld20.12.pass.sdf.gz
#  split by '.' yields [zld20, 12/zld20, 12, pass, sdf, gz]
#  position *3* would be 12
#
#  compare the list of completed jobs to a completed list of reference numbers
#  to find out which jobs (numbers) are incomplete (missing)
#
#  print out the incomplete job names by substituting a string
#
######################################################################
