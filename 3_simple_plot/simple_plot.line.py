#!/usr/bin/env python3

##########################################################################
#
#  Peter MU Ung @ MSSM/Yale
#
#  v1.   19.12.27
#
#  Do very simple line plot for one data file or multiple data files with
#  same file extension.
#
##########################################################################

import sys
msg = '''\n\t> {0}
\t\t[ -a: Plot for all data files with Extension (e.g.: .txt) ]
\t\t[ -f: Plot for one data file ]
\t\t\t[ Optional: Running in Serial? (Def: 0) ]\n
e.g.> *.py  -a .txt 
  or
    > *.py  -f data.txt 1\n'''.format(sys.argv[0])
if len(sys.argv) < 2: sys.exit(msg)

try:
  serial = sys.argv[4]
except IndexError:
  serial = 0
  print('  Running in Parallel\n')

import re,glob
import numpy as np
import pandas as pd
import seaborn as sns

import matplotlib
matplotlib.use('Agg')   # to get around Xwindows when over 'ssh'

import matplotlib.pyplot as plt
from pathos import multiprocessing
  
################################################
def main():

  if re.search('-a', sys.argv[1]):
    file_list = glob.glob('*'+sys.argv[2])
    snsp = plot_fig(ext=sys.argv[2])

    if not serial:
      mpi = multiprocessing.Pool(processes=len(file_list))
      mpi.map(snsp, file_list)
      mpi.close()
      mpi.join()
    else:
      xxx = [snsp(name) for name in file_list]
  
  else:
    ext = sys.argv[2].split('.')[-1]
    snsp = plot_fig(ext='.'+ext)
    snsp(sys.argv[2])


###########################################################################
###########################################################################

def running_avg(x, N):
  cumsum = np.cumsum(np.insert(x, 0.0, 0.0))
  return (cumsum[N:] - cumsum[:-N])/ float(N)


####################
class plot_fig(object):
  def __init__(self, ext=''):
    self.ext = ext
  def __call__(self, inp):
    return self.sns_plot(inp)

  def sns_plot(self, inp):

    data = pd.read_csv( inp, delimiter='\s+', skipinitialspace=True )
    print(inp.split(self.ext))
    fname = inp.split(self.ext)[0]
    y = data[data.columns[1]]

    if len(data) <= 50:
      N = 5
    elif len(data) <= 100:
      N = 10
    elif len(data) <= 500:
      N = 25
    elif len(data) <= 1000:
      N = 50
    else:
      N = 100

    y1 = y.rolling(window=N).median().iloc[N-1:].values
    y2 = pd.DataFrame(y1, columns=[data.columns[1]])

    data2 = pd.concat([ data[data.columns[0]], y2  ], axis=1)
    sns.set(rc={"lines.linewidth": 0.33})
    ax = sns.lineplot(x=data2.columns[0], y=data2.columns[1], data=data2,
                      ci='sd', err_style='band')

    plt.savefig(fname+'.png', dpi=150, figsize=(8,6))


######################################################################
if __name__ == '__main__':
  main()
