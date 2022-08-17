#!/usr/bin/env python3

##########################################################################
#
#  Peter MU Ung @ MSSM/Yale/gRED
#
#  v1.   19.12.27
#  v2    22.07.15 @ gRED allow plotting multiple lines at once
#
#  Do very simple line plot for one data file or multiple data files with
#  same file extension. Data is averaged using a moving window of variable
#  size, depending on the size of the data available
#
##########################################################################

import sys
msg = '''\n\t> {0}
    -a < >     [ Plot for all data files with Extension (e.g.: .txt)  ]
    -i <+>     [ Plot for one/more data file (e.g.: filename.txt.bz2) ]
    -o < >     [ Ouptut plot prefix ]
  Optional:
    -n <+>     [ Custom Colnames matching data file order (e.g.: x_id y_id z_id) ]
    -d < >     [ Delimiter       (Def:"\s+") ]
    -x < >     [ Name for x-axis (Def: None) ]
    -y < >     [ Name for y-axis (Def: None) ]
    -t < >     [ Name for title  (Def: None) ]
    -l <+>     [ Set (bottom top) y-limits (Def: None) ]
    -s         [ Running in Serial (Def: False) ]
    -m         [ Adaptive moving-window smoothing (Def: False) ]
    -w < >     [ Linewidth (Def: 1.0) ]
    -ver <+>   [ Add vertical line(s), x = input (def: None) ]
    -hor <+>   [ Add horizontal line(s), y = input (def: None) ]
    -col <+>   [ Vertical/Horizontal line color (def="red") ]
    -rot < >   [ Rotate x-tick label by degree (Def: 0 | 33 is good) ]
    -img < >   [ Figure format: png|jpg|svg|eps|pdf (Def: png) ]
    -siz <+>   [ Figure x/y dimension in inch (Def: 8 6) ]
    -dpi < >   [ Figure quality (Def: 150) ]\n
e.g.> *.py  -a '.txt'
  or
    > *.py  -i data.txt -s -m\n'''.format(sys.argv[0])
if len(sys.argv) == 1: sys.exit(msg)

import glob
import matplotlib
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

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
    snsp = plot_fig(ext=args.ext, sep=args.sep, mv_avg=args.mv_avg,
                    x_name=args.x_name, y_name=args.y_name, column=args.col,
                    title=args.title, y_lim=y_lim, size=size, linewidth=args.linewidth,
                    rotate=args.rotate)

    if not args.serial:
      mpi = multiprocessing.Pool(processes=len(file_list))
      mpi.map(snsp, file_list)
      mpi.close()
      mpi.join()
    else:
      xxx = [snsp(name) for name in file_list]
  
  else:
    if not args.infile: sys.exit('\033[31m  ERROR:\033[0m No input file\n')
#    ext = args.infile.split('.')[-1]
    snsp = plot_fig(sep=args.sep, mv_avg=args.mv_avg,
                    x_name=args.x_name, y_name=args.y_name, title=args.title,
                    col_names=args.col_names, y_lim=y_lim, linewidth=args.linewidth,
                    img=args.img, dpi=args.dpi, size=size, outpref=args.outpref,
                    rotate=args.rotate, vlines=args.vlines, hlines=args.hlines,
                    refcolr=args.refcolr )
    snsp(args.infile)


###########################################################################

class plot_fig(object):
  def __init__( self, sep='', ext='', x_name='', y_name='', title='', y_lim='',
                      col=0, col_names=[], mv_avg='', img='', dpi='', size='',
                      linewidth='', rotate=0, outpref='', vlines=[], hlines=[],
                      refcolr='red' ):
    self.ext = ext
    self.sep = sep
    self.col = col
    self.title = title
    self.x_name = x_name
    self.y_name = y_name
    self.col_names = col_names
    self.mv_avg = mv_avg
    self.y_lim  = y_lim
    self.vlines = vlines
    self.hlines = hlines
    self.refcolr= refcolr
    self.img    = img
    self.dpi    = dpi
    self.size   = size
    self.rotate = rotate
    self.linewidth = linewidth
    self.outpref = outpref

  def __call__(self, inp):
    return self.sns_plot(inp)

  def sns_plot(self, inp):

    df_list = [ pd.read_csv(f, sep=self.sep, skipinitialspace=True) for f in inp ]

    ## smoothing input with adaptive moving window averaging
    if self.mv_avg:
      avg_list = []
      for df in df_list:
        y  = df.iloc[:, int(self.col)-1]
        N  = AdaptiveMovingWindow(len(y))
        y1 = y.rolling(window=N).median().iloc[N-1:].values
        y2 = pd.DataFrame(y1, columns=[df.columns[1]])
        avg_list.append( pd.concat([ df[df.columns[0]], y2 ], axis=1) )
        print('# Adaptive Moving Window: {0}'.format(N))
      df_list = avg_list


    ## combine list of Dataframes into one single dataframe
    data = df_list[0]
    for df in df_list[1:]:
      data = pd.merge(data, df, on=data.columns[0], how='outer')
    xdf = data.set_index(data.columns[0])

    ## change data column name, if applicable
    if self.col_names:
      xdf.columns = self.col_names


    ## Plot data as line plot
    sns.set(rc={"lines.linewidth": float(self.linewidth)}, style='whitegrid')
    fig, ax = plt.subplots()
    fig.set_size_inches(tuple(self.size))

    ax = sns.lineplot(data=xdf, ci='sd', err_style='band')

    ## Add custom vertical/horizontal lines
    if self.vlines:
      for i, v in enumerate(self.vlines):
        ax.axvline(x=float(v), color=self.refcolr[i], lw=float(self.linewidth))
    if self.hlines:
      for i, h in enumerate(self.hlines):
        ax.axhline(y=float(h), color=self.refcolr[i], lw=float(self.linewidth))

    ## Adjust labels, titles, max_y-axis
    ax.set(xlabel=self.x_name, ylabel=self.y_name)
    ax.tick_params(axis='x', rotation=int(self.rotate))
    if self.title: ax.set_title(self.title)
    if self.y_lim is not None: ax.set(ylim=tuple(self.y_lim))

    plt.savefig('{0}.{1}.{2}'.format(self.outpref, 'line', self.img),
                    format=self.img, dpi=int(self.dpi) )
    plt.clf()


######################################################################
## coefficient for Adaptive moving window smoothing
def AdaptiveMovingWindow( row_num ):
  if   row_num <= 50:
    return 5
  elif row_num <= 100:
    return 10
  elif row_num <= 500:
    return 25
  elif row_num <= 1000:
    return 50
  else:
    return 100


###########################################################################

def running_avg(x, N):
  cumsum = np.cumsum(np.insert(x, 0.0, 0.0))
  return (cumsum[N:] - cumsum[:-N])/ float(N)


######################################################################
def UserInput():
  p = ArgumentParser(description='Command Line Arguments')

  p.add_argument('-a', dest='ext', required=False, default=False,
                  help='Plot for all data files with Extension (e.g.: .txt)')
  p.add_argument('-i', dest='infile', required=False, nargs='+', default=False,
                  help='Plot for one/more data file (e.g.: filename.txt.bz2)')
  p.add_argument('-o', dest='outpref', required=True,
                  help='Output plot file prefix')
  p.add_argument('-d', dest='sep', required=False, default='\s+',
                  help='delimiter       (Def:"\s+")')
  p.add_argument('-c', dest='col', required=False, default=0,
                  help='Column in file(s) to be plotted (Def: last column)')
  p.add_argument('-n', dest='col_names', required=False, nargs="+", default=None,
                  help='Custom Column names (e.g.: x_dist y_dist z_dist)')
  p.add_argument('-x', dest='x_name', required=False, default='',
                  help='Name for x-axis (Def: "")')
  p.add_argument('-y', dest='y_name', required=False, default='',
                  help='Name for y-axis (Def: "")')
  p.add_argument('-t', dest='title', required=False, default='',
                  help='Name for title  (Def: "")')
  p.add_argument('-l', dest='y_lim', required=False, nargs="+", default=None,
                  help='Set (bottom top) y-limits (Def: None)')

  p.add_argument('-w', dest='linewidth', required=False, default=1.0,
                  help='Line width (Def: 1.0)')
  p.add_argument('-ver', dest='vlines', required=False, nargs='+', default=[],
                  help='Add vertical line(s), x = input (Def: None)')
  p.add_argument('-hor', dest='hlines', required=False, nargs='+', default=[],
                  help='Add horizontal line(s), y = input (Def: None)')
  p.add_argument('-col', dest='refcolr',required=False, default=['r'], nargs='+',
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
  p.add_argument('-m', dest='mv_avg', action='store_true',
                  help='Adaptive moving-window smoothing (Def: False)')

  args=p.parse_args()
  return args

######################################################################
if __name__ == '__main__':
  main()
