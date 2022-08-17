#!/usr/bin/env python3

##########################################################################
#
#  Peter MU Ung @ MSSM/Yale/gRED
#
#  v1.	19.12.27
#  v2	  21.06.25  update to use Histogram function
#
#  Do very simple histogram for one data file or multiple data files with
#  same file extension.
#
##########################################################################

import sys
msg = '''\n\t> {0}
    -a < >     [ Plot for all data files with Extension (e.g.: .txt) ]
    -f < >     [ Plot for one data file (e.g.: filename.txt.bz2)     ]
  Optional:
    -s         [ Running in Serial (Def: False ]
    -norm      [ Normalize data  (Def: False) ]
    -d < >     [ Delimiter       (Def:"\s+") ]
    -c < >     [ Column to be analyzed (Def: 1) ]
    -x < >     [ Name for x-axis (Def: None) ]
    -y < >     [ Name for y-axis (Def: None) ]
    -t < >     [ Name for title  (Def: None) ]
    -l <+>     [ Set (bottom top) y-limits (Def: None) ]
    -bin < >   [ Bin number      (Def: auto) ]
    -w   < >   [ Line width (Def: 1.0) ]
    -ver <+>   [ Add vertical line(s), x = input (def: None) ]
    -hor <+>   [ Add horizontal line(s), y = input (def: None) ]
    -col < >   [ Vertical/Horizontal line color (def="red") ]
    -img < >   [ Figure format: png|jpg|svg|eps|pdf (Def: png) ]
    -siz <+>   [ Figure x/y dimension in inch (Def: 8 6) ]
    -dpi < >   [ Figure quality (Def: 150) ]\n
e.g.> *.py  -a '.txt'
  or
    > *.py  -f data.txt -s\n'''.format(sys.argv[0])
if len(sys.argv) == 1: sys.exit(msg)

import glob
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
  if args.size:
    size  = np.array(args.size, dtype=np.float32)
  else:
    size  = args.size

###################################

  if args.ext:
    file_list = glob.glob('*'+args.ext)
    if not file_list: sys.exit('\033[31m  ERROR:\0330m No file matches Extension\n')
    snsp = plot_fig(ext=args.ext, col=int(args.col), sep=args.sep, size=size,
                    img=args.img, dpi=int(args.dpi), bins=int(args.bins), norm=args.norm,
                    x_name=args.x_name, y_name=args.y_name, title=args.title, y_lim=y_lim,
                    linewidth=args.linewidth, vlines=args.vlines, hlines=args.hlines, 
                    refcolr=args.refcolr)

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
    snsp = plot_fig(ext='.'+ext, col=int(args.col), sep=args.sep, img=args.img,
                    bins=int(args.bins), norm=args.norm, size=size, linewidth=args.linewidth,
                    x_name=args.x_name, y_name=args.y_name, title=args.title, y_lim=y_lim,
                    vlines=args.vlines, hlines=args.hlines, refcolr=args.refcolr)
    snsp(args.infile)



###########################################################################
###########################################################################

class plot_fig(object):
  def __init__( self, sep='', ext='', x_name='', y_name='', title='', y_lim='',
                      norm=0, bins='',col=1,  img='png', dpi=150, size=(), 
                      linewidth='', vlines=[], hlines=[], refcolr=''):
    self.ext = ext
    self.sep = sep
    self.col = col
    self.bins = bins
    self.norm = norm
    self.title = title
    self.x_name = x_name
    self.y_name = y_name
    self.y_lim  = y_lim
    self.vlines = vlines
    self.hlines = hlines
    self.refcolr= refcolr
    self.dpi    = dpi
    self.img    = img
    self.size   = size
    self.linewidth = linewidth

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

    sns.set(rc={"lines.linewidth": float(self.linewidth)})
    fig, ax = plt.subplots()
    fig.set_size_inches(tuple(self.size))

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

    ## Add custom vertical/horizontal lines
    if self.vlines:
      for v in self.vlines:
        ax.axvline(x=float(v), color=self.refcolr, lw=float(self.linewidth))
    if self.hlines:
      for h in self.hlines:
        ax.axhline(y=float(h), color=self.refcolr, lw=float(self.linewidth))

    ## Adjust labels, titles, max_y-axis
    ax.set(xlabel=self.x_name, ylabel=self.y_name)
    if self.title: ax.set_title(self.title)
    if self.y_lim is not None: ax.set(ylim=tuple(self.y_lim))

    plt.savefig('{0}.histo.{1}'.format(fname, self.img),
                      format=self.img, dpi=self.dpi)
    plt.clf()
    

######################################################################
def UserInput():
  p = ArgumentParser(description='Command Line Arguments')

  p.add_argument('-a', dest='ext', required=False, default=False,
                  help='Plot for all data files with Extension (e.g.: .txt)')
  p.add_argument('-f', dest='infile', required=False, default=False,
                  help='Plot for one data file (e.g.: filename.txt.bz2)')

  p.add_argument('-d', dest='sep', required=False, default='\s+',
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

  p.add_argument('-w', dest='linewidth', required=False, default=1.0,
                  help='Line width (Def: 1.0)')
  p.add_argument('-ver', dest='vlines', required=False, nargs='+', default=[],
                  help='Add vertical line(s), x = input (Def: None)')
  p.add_argument('-hor', dest='hlines', required=False, nargs='+', default=[],
                  help='Add horizontal line(s), y = input (Def: None)')
  p.add_argument('-col', dest='refcolr',required=False, default='red',
                  help='Vertical/Horizontal line color (def="red")')

  p.add_argument('-img', dest='img', required=False, default='png',
                  help='Figure format: png|jpg|svg|eps|pdf (Def: png)')
  p.add_argument('-dpi', dest='dpi', required=False, default=150,
                  help='Figure quality  (Def: 150)')
  p.add_argument('-siz', dest='size', required=False, nargs='+', default=[8,6],
                  help='Figure x/y dimensions in inch  (Def: 8 6)')

  p.add_argument('-s', dest='serial', action='store_true',
                  help='Running in Serial (Def: False)')
  p.add_argument('-norm', dest='norm', action='store_true',
                  help='Normalize the data (Def: False)')

  args=p.parse_args()
  return args

######################################################################
if __name__ == '__main__':
  main()
