#!/usr/bin/env python3

##########################################################################
#
#  Peter MU Ung @ MSSM/Yale
#
#  v1.   19.12.27
#
#  Do very simple 2D-scatter plot for one or multiple data files with
#  same file extension.
#
##########################################################################

import sys
msg = '''\n\t> {0}
\t-a < >     [ Plot for all data files with Extension (e.g.: .txt) ] only first 2 cols
\t-f < >     [ Plot for one data file (e.g.: filename.txt.bz2)     ]
\tOptional:
\t-d < >     [ Delimiter       (Def:"\s+") ]
\t-x < >     [ Name for x-axis (Def: None) ]
\t-y < >     [ Name for y-axis (Def: None) ]
\t-t < >     [ Name for title  (Def: None) ]
\t-l <+>     [ Set (bottom top) y-limits (Def: None) ]
\t-den       [ Plot as density (Def: False) ]
\t-s         [ Running in Serial (Def: False) ]
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

from pathos import multiprocessing
from argparse import ArgumentParser

################################################
def main():

  args = UserInput()
  print('')
  if args.ext:
    ext = args.ext
    print('-a', ext)
  else:
    ext = False
  if args.infile: 
    infile = args.infile
    print('-f', infile)
  else:
    infile = False

  if args.delimiter:
    delimiter = args.delimiter
    print('-d', delimiter)
  else:
    delimiter = '\s+'

  if args.x_name:
    x_name = args.x_name
    print('-x', x_name)
  else:
    x_name = False

  if args.y_name:
    y_name = args.y_name
    print('-y', y_name)
  else:
    y_name = False

  if args.y_lim:
    y_lim = np.array(args.y_lim, dtype=np.float32)
    print('-l', y_lim)
  else:
    y_lim = None

  if args.title:
    title = args.title
    print('-t', title)
  else:
    title = False

  if args.density:
    density = True
  else:
    density = False

  serial = args.serial
  if args.img:
    img = args.img
  else:
    img = 'png'
  if args.dpi:
    dpi = int(args.dpi)
  else:
    dpi = 150

  if ext:
    file_list = glob.glob('*'+ext)
    if not file_list: sys.exit('\033[31m  ERROR:\0330m No file matches Extension\n')
    snsp = plot_fig(  ext=ext, sep=delimiter, 
                      x_name=x_name, y_name=y_name, title=title,
                      y_lim=y_lim, density=density,
                      dpi=dpi, img=img )

    if not serial:
      mpi = multiprocessing.Pool(processes=len(file_list))
      mpi.map(snsp, file_list)
      mpi.close()
      mpi.join()
    else:
      xxx = [snsp(name) for name in file_list]

  else:
    if not infile: sys.exit('\033[31m  ERROR:\033[0m No input file\n')
    ext = infile.split('.')[-1]
    snsp = plot_fig(  ext='.'+ext, sep=delimiter, 
                      x_name=x_name, y_name=y_name, title=title, 
                      y_lim=y_lim, density=density,
                      dpi=dpi, img=img )
    snsp(infile)



###########################################################################
###########################################################################

class plot_fig(object):
  def __init__( self, sep='', ext='', x_name='', y_name='', title='', 
                      y_lim='', density='', dpi='', img='' ):
    self.ext = ext
    self.sep = sep
    self.img = img
    self.dpi = dpi
    self.title = title
    self.x_name = x_name
    self.y_name = y_name
    self.y_lim  = y_lim
    self.density = density

  def __call__(self, inp):
    return self.sns_plot(inp)

  def sns_plot(self, inp):

    data = pd.read_csv( inp, delimiter=self.sep, skipinitialspace=True )
    print(inp.split(self.ext))
    fname = inp.split(self.ext)[0]

    names = data.columns
    if not self.x_name: self.x_name = names[0]
    if not self.y_name: self.y_name = names[1]

    sns.set(rc={"lines.linewidth": 1.0})

    if not self.density:
      ax = sns.jointplot( x=self.x_name, y=self.y_name, data=data.iloc[:,0:2],
                          alpha=0.5 )
    else:
      ax = sns.jointplot( x=self.x_name, y=self.y_name, data=data.iloc[:,0:2],
                          kind='kde' )

#    ax.set(xlabel=self.x_name, ylabel=self.y_name)
    if self.title: ax.set_title(self.title)
    if self.y_lim is not None: ax.set(ylim=self.y_lim)

    plt.savefig('{0}.scatter.{1}'.format(fname, self.img), figsize=(8,6),
                    format=self.img, dpi=self.dpi)
    plt.clf()


######################################################################
def UserInput():
  p = ArgumentParser(description='Command Line Arguments')

  p.add_argument('-a', dest='ext', required=False,
                  help='Plot for all data files with Extension (e.g.: .txt)')
  p.add_argument('-f', dest='infile', required=False,
                  help='Plot for one data file (e.g.: filename.txt.bz2)')
  p.add_argument('-d', dest='delimiter', required=False,
                  help='delimiter       (Def:"\s+")')
  p.add_argument('-x', dest='x_name', required=False,
                  help='Name for x-axis (Def: None)')
  p.add_argument('-y', dest='y_name', required=False,
                  help='Name for y-axis (Def: None)')
  p.add_argument('-t', dest='title', required=False,
                  help='Name for title  (Def: None)')
  p.add_argument('-l', dest='y_lim', required=False, nargs="+",
                  help='Set (bottom top) y-limits (Def: None)')
  p.add_argument('-img', dest='img', required=False,
                  help='Figure format: png|jpg|svg|eps|pdf (Def: png)')
  p.add_argument('-dpi', dest='dpi', required=False,
                  help='Figure quality  (Def: 150)')

  p.add_argument('-s', dest='serial', action='store_true',
                  help='Running in Serial (Def: False)')
  p.add_argument('-den', dest='density', action='store_true',
                  help='Plot as density (Def: False)')

  args=p.parse_args()
  return args

######################################################################
if __name__ == '__main__':
  main()
