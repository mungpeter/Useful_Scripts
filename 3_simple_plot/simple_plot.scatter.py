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
    -a < >     [ Plot for all data files with Extension (e.g.: .txt) ] only first 2 cols
    -i < >     [ Plot for one data file (e.g.: filename.txt.bz2)     ]
  Optional:
    -d < >     [ Delimiter       (Def:"\s+") ]
    -x < >     [ Name for x-axis (Def: None) ]
    -y < >     [ Name for y-axis (Def: None) ]
    -t < >     [ Name for title  (Def: None) ]
    -l <+>     [ Set (bottom top) y-limits (Def: None) ]
    -den       [ Plot as density (Def: False) ]
    -s         [ Running in Serial (Def: False) ]
    -w < >     [ Linewidth (Def: 1.0) ]
    -ver <+>   [ Add vertical line(s), x = input (def: None) ]
    -hor <+>   [ Add horizontal line(s), y = input (def: None) ]
    -col < >   [ Vertical/Horizontal line color (def="red") ]
    -rot < >   [ Rotate x-tick label by degree (Def: 0 | 33 is good) ]
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
  if args.ext:
    ext = args.ext
    print('-a', ext)
  else:
    ext = False
  if args.infile: 
    infile = args.infile
    print('-i', infile)
  else:
    infile = False

  if args.y_lim:
    y_lim = np.array(args.y_lim, dtype=np.float32)
    print('-l', y_lim)
  else:
    y_lim = None

  serial = args.serial
  if args.size:
    size  = np.array(args.size, dtype=np.float32)
  else:
    size  = args.size

###################################

  if ext:
    file_list = glob.glob('*'+ext)
    if not file_list: sys.exit('\033[31m  ERROR:\0330m No file matches Extension\n')
    snsp = plot_fig(  ext=ext, sep=args.sep, 
                      x_name=args.x_name, y_name=args.y_name, title=args.title,
                      y_lim=args.y_lim, density=args.density, rotate=args.rotate,
                      dpi=args.dpi, img=args.img, size=size, linewidth=args.linewidth,
                      vlines=args.vlines, hlines=args.hlines, refcolr=args.refcolr )

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
    snsp = plot_fig(  ext='.'+ext, sep=args.sep, 
                      x_name=args.x_name, y_name=args.y_name, title=args.title, 
                      y_lim=args.y_lim, density=args.density, rotate=args.rotate,
                      dpi=args.dpi, img=args.img, size=size, linewidth=args.linewidth,
                      vlines=args.vlines, hlines=args.hlines, refcolr=args.refcolr )
    snsp(infile)



###########################################################################
###########################################################################

class plot_fig(object):
  def __init__( self, sep='', ext='', x_name='', y_name='', title='', 
                      y_lim='', density='', dpi='', img='', size='',
                      linewidth='', rotate='', vlines=[], hlines=[],
                      refcolr='' ):
    self.ext = ext
    self.sep = sep
    self.img = img
    self.dpi = dpi
    self.size = size
    self.title = title
    self.x_name = x_name
    self.y_name = y_name
    self.y_lim  = y_lim
    self.density = density
    self.linewidth = linewidth
    self.rotate = rotate
    self.vlines = vlines
    self.hlines = hlines
    self.refcolr= refcolr

  def __call__(self, inp):
    return self.sns_plot(inp)

  def sns_plot(self, inp):

    data = pd.read_csv( inp, delimiter=self.sep, skipinitialspace=True )
    print(inp.split(self.ext))
    fname = inp.split(self.ext)[0]

    names = data.columns
    if not self.x_name: self.x_name = names[0]
    if not self.y_name: self.y_name = names[1]

    sns.set(rc={"lines.linewidth": float(self.linewidth)})
    fig, ax = plt.subplots()
    fig.set_size_inches(tuple(self.size))


    if not self.density:
      ax = sns.jointplot( x=self.x_name, y=self.y_name, data=data.iloc[:,0:2],
                          alpha=0.5 )
    else:
      ax = sns.jointplot( x=self.x_name, y=self.y_name, data=data.iloc[:,0:2],
                          kind='kde' )

    ## Add custom vertical/horizontal lines
    if self.vlines:
      for v in self.vlines:
        ax.refline(x=float(v), color=self.refcolr, lw=float(self.linewidth))
    if self.hlines:
      for h in self.hlines:
        ax.refline(y=float(h), color=self.refcolr, lw=float(self.linewidth))

    ## Adjust labels, titles, max_y-axis
    ax.set(xlabel=self.x_name, ylabel=self.y_name)
    ax.set_xticklabels(ax.get_xticklabels(), rotation=int(args.rotate))
    if self.title: ax.set_title(self.title)
    if self.y_lim is not None: ax.set(ylim=self.y_lim)

    plt.savefig('{0}.scatter.{1}'.format(fname, self.img),
                    format=self.img, dpi=int(self.dpi))
    plt.clf()


######################################################################
def UserInput():
  p = ArgumentParser(description='Command Line Arguments')

  p.add_argument('-a', dest='ext', required=False,
                  help='Plot for all data files with Extension (e.g.: .txt)')
  p.add_argument('-i', dest='infile', required=False,
                  help='Plot for one data file (e.g.: filename.txt.bz2)')
  p.add_argument('-d', dest='sep', required=False, default='\s+',
                  help='delimiter       (Def:"\s+")')
  p.add_argument('-x', dest='x_name', required=False, default=False,
                  help='Name for x-axis (Def: None)')
  p.add_argument('-y', dest='y_name', required=False, default=False,
                  help='Name for y-axis (Def: None)')
  p.add_argument('-t', dest='title', required=False, default=False,
                  help='Name for title  (Def: None)')
  p.add_argument('-l', dest='y_lim', required=False, nargs="+",
                  help='Set (bottom top) y-limits (Def: None)')

  p.add_argument('-w', dest='linewidth', required=False, default=1.0,
                  help='Line width (Def: 1.0)')
  p.add_argument('-ver', dest='vlines', required=False, nargs='+', default=[],
                  help='Add vertical line(s), x = input (Def: None)')
  p.add_argument('-hor', dest='hlines', required=False, nargs='+', default=[],
                  help='Add horizontal line(s), y = input (Def: None)')
  p.add_argument('-col', dest='refcolr',required=False, default='red',
                  help='Vertical/Horizontal line color (def="red")')

  p.add_argument('-rot', dest='rotate', required=False, default=0,
                  help='Rotate x-tick label by degree (Def: 0 | 33 is good)')
  p.add_argument('-img', dest='img', required=False, default='png',
                  help='Figure format: png|jpg|svg|eps|pdf (Def: png)')
  p.add_argument('-dpi', dest='dpi', required=False, default=150,
                  help='Figure quality  (Def: 150)')
  p.add_argument('-siz', dest='size', required=False, nargs='+', default=[8,6],
                  help='Figure x/y dimensions in inch  (Def: 8 6)')

  p.add_argument('-s', dest='serial', action='store_true',
                  help='Running in Serial (Def: False)')
  p.add_argument('-den', dest='density', action='store_true',
                  help='Plot as density (Def: False)')

  args=p.parse_args()
  return args

######################################################################
if __name__ == '__main__':
  main()
