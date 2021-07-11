#!/usr/bin/env python3

##########################################################################
#
#  Peter MU Ung @ MSSM/Yale
#
#  v1.	19.12.27
#  v2	21.06.25  update to use Histogram function
#
#  Do very simple histogram for one data file or multiple data files with
#  same file extension.
#
##########################################################################

import sys
msg = '''\n\t> {0}
\t-a < >     [ Plot for all data files with Extension (e.g.: .txt) ]
\t-f < >     [ Plot for one data file (e.g.: filename.txt.bz2)     ]
\tOptional:
\t-s         [ Running in Serial (Def: False ]
\t-norm      [ Normalize data  (Def: False) ]
\t-d < >     [ Delimiter       (Def:"\s+") ]
\t-c < >     [ Column to be analyzed (Def: 1) ]
\t-x < >     [ Name for x-axis (Def: None) ]
\t-y < >     [ Name for y-axis (Def: None) ]
\t-t < >     [ Name for title  (Def: None) ]
\t-l <+>     [ Set (bottom top) y-limits (Def: None) ]
\t-bin < >   [ Bin number      (Def: auto) ]
\t-img < >   [ Figure format: png|jpg|svg|eps|pdf (Def: png) ]
\t-dpi < >   [ Figure quality (Def: 150) ]\n
e.g.> *.py  -a '.txt'
  or
    > *.py  -f data.txt -s\n'''.format(sys.argv[0])
if len(sys.argv) == 1: sys.exit(msg)

import re,glob
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

sns.set(color_codes=True)
matplotlib.use('Agg')   # to get around Xwindows when over 'ssh'

import multiprocessing
from argparse import ArgumentParser

################################################
def main():

  args = UserInput()
  print('')

  if args.y_lim:
    y_lim = np.array(args.y_lim, dtype=np.float32)
    print('-l', y_lim)
  else:
    y_lim = None



  if args.ext:
    file_list = glob.glob('*'+args.ext)
    if not file_list: sys.exit('\033[31m  ERROR:\0330m No file matches Extension\n')
    snsp = plot_fig(ext=args.ext, col=int(args.col), sep=args.delimiter, 
                    img=args.img, dpi=int(args.dpi), bins=int(args.bins), norm=args.norm,
                    x_name=args.x_name, y_name=args.y_name, title=args.title, y_lim=y_lim,)

    if not args.serial:
      mpi = multiprocessing.Pool(processes=len(file_list))
      mpi.map(snsp, file_list)
      mpi.close()
      mpi.join()
    else:
      xxx = [snsp(name) for name in file_list]
  
  else:
    if not args.infile: sys.exit('\033[31m  ERROR:\033[0m No input file\n')
    ext = args.infile.split('.')[-1]
    snsp = plot_fig(ext='.'+ext, col=int(args.col), sep=args.delimiter, img=args.img,
                    bins=int(args.bins), norm=args.norm,
                    x_name=args.x_name, y_name=args.y_name, title=args.title, y_lim=y_lim)
    snsp(args.infile)



###########################################################################
###########################################################################

class plot_fig(object):
  def __init__( self, sep='', ext='', x_name='', y_name='', title='', y_lim='',
                      norm=0,bins='',col=1,  img='png', dpi=150 ):
    self.ext = ext
    self.sep = sep
    self.col = col
    self.bins = bins
    self.norm = norm
    self.title = title
    self.x_name = x_name
    self.y_name = y_name
    self.y_lim  = y_lim
    self.dpi    = dpi
    self.img    = img

  def __call__(self, infile):
    return self.sns_plot(infile)

  def sns_plot(self, infile):

    data = pd.read_csv( infile, delimiter=self.sep, skipinitialspace=True )
    print(data.iloc[:,self.col-1])
    print(infile.split(self.ext))
    fname = infile.split(self.ext)[0]

    names = data.columns
    if not self.x_name: self.x_name = names[0]
    if not self.y_name: self.y_name = names[1]

    sns.set(rc={"lines.linewidth": 1.0})
    if self.bins:
      if self.norm:
        ax = sns.histplot(data.iloc[:,self.col-1], bins=self.bins, stat='probability')
      else:
        ax = sns.histplot(data.iloc[:,self.col-1], bins=self.bins)
    else:
      if self.norm:  
        ax = sns.histplot(data.iloc[:,self.col-1], stat='probability')
      else:
        ax = sns.histplot(data.iloc[:,self.col-1])

    ax.set(xlabel=self.x_name, ylabel=self.y_name)
    if self.title: ax.set_title(self.title)
    if self.y_lim is not None: ax.set(ylim=self.y_lim)

    plt.savefig('{0}.histo.{1}'.format(fname, self.img), figsize=(8,6),
                      format=self.img, dpi=self.dpi)
    plt.clf()
    

######################################################################
def UserInput():
  p = ArgumentParser(description='Command Line Arguments')

  p.add_argument('-a', dest='ext', required=False, default=False,
                  help='Plot for all data files with Extension (e.g.: .txt)')
  p.add_argument('-f', dest='infile', required=False, default=False,
                  help='Plot for one data file (e.g.: filename.txt.bz2)')

  p.add_argument('-d', dest='delimiter', required=False, default='\s+',
                  help='delimiter       (Def: "\s+")')
  p.add_argument('-c', dest='col', required=False, default=1,
                  help='Column to be analyzed (Def: 1)')
  p.add_argument('-x', dest='x_name', required=False, default=False,
                  help='Name for x-axis (Def: None)')
  p.add_argument('-y', dest='y_name', required=False, default=False,
                  help='Name for y-axis (Def: None)')
  p.add_argument('-t', dest='title', required=False, default=False,
                  help='Name for title  (Def: None)')
  p.add_argument('-l', dest='y_lim', required=False, nargs="+", default='',
                  help='Set (bottom top) y-limits (Def: None)')
  p.add_argument('-bin',dest='bins', required=False, default=None,
                  help='Bin number (Def: auto)')
  p.add_argument('-img', dest='img', required=False, default='png',
                  help='Figure format: png|jpg|svg|eps|pdf (Def: png)')
  p.add_argument('-dpi', dest='dpi', required=False, default=150,
                  help='Figure quality  (Def: 150)')

  p.add_argument('-s', dest='serial', action='store_true',
                  help='Running in Serial (Def: False)')
  p.add_argument('-norm', dest='norm', action='store_true',
                  help='Normalize the data (Def: False)')

  args=p.parse_args()
  return args

######################################################################
if __name__ == '__main__':
  main()
