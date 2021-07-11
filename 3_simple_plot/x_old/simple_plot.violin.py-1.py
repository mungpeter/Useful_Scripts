#!/usr/bin/env python3

##########################################################################
#
#  Peter MU Ung @ MSSM/Yale
#
#  v1.   19.12.27
#
#  Do very simple violin-type histogram for *multiple* data files at once
#
##########################################################################

import sys
msg = '''\n  > {0}
\t-i <+>     [ Data file(s) ] # separated by space; 1 or 2 columns; only use last col
\t-o < >     [ Output prefix ]
\tOptional:
\t-n <+>     [ Column name (Def: from header) ]
\t-d < >     [ Delimiter       (Def:'\s+') ]
\t-x < >     [ Name for x-axis (Def: None) ]
\t-y < >     [ Name for y-axis (Def: None) ]
\t-t < >     [ Name for title  (Def: None) ]
\t-l <+>     [ Set (bottom top) y-limits (Def: None) ]
\t-p         [ Use Plotnine plotting method (Def: Seaborn) ]
\t-img < >   [ Figure format: png|jpg|svg|eps|pdf (Def: png) ]
\t-dpi < >   [ Figure quality (Def: 150) ]\n
e.g.> *.py   -i x.txt y.txt z.txt    -o output\n'''.format(sys.argv[0])
if len(sys.argv) == 1: sys.exit(msg)

import re,glob
import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

matplotlib.use('Agg')   # to get around Xwindows when over 'ssh'

from argparse import ArgumentParser

################################################
def main():

  args = UserInput()
  print('')
  if args.infile:
    infile = args.infile
    print('-i', infile)
  if args.outpref: 
    outpref = args.outpref
    print('-o', outpref)

  if args.col_names:
    col_names = args.col_names
    print('-n', col_names)
  else:
    col_names = False

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

  use_p9 = args.use_p9
  if args.img:
    img = args.img
  else:
    img = 'png'
  if args.dpi:
    dpi = int(args.dpi)
  else:
    dpi = 150

###################################
  df_list = [ pd.read_csv(f, delimiter=delimiter, skipinitialspace=True) 
                for f in infile ]

  ## only take input with 1 or 2 columns; for 2 columns, 1st is always removed
  lg_list = []
  for idx, df in enumerate(df_list):
    if len(df.columns) > 2:
      sys.exit('\033[34m  ERROR:\033[m Only take inputs with 1 or 2 columns')

    if len(df.columns) == 1:
      if col_names:
        df.columns = [col_names[idx]]
    if len(df.columns) == 2:
      if col_names:
        df.columns = ['frame', col_names[idx]]
      else:
        df.columns = ['frame', df.columns[1]]
      df.drop(columns=['frame'], inplace=True)

    lg_list.append(pd.melt(df))
  lg_df = pd.concat(lg_list)
  lg_df.columns = [x_name, y_name]


  ## plotnine method
  if use_p9:
    import plotnine as p9
    Quant = [.25,.5,.75]

    if y_lim is not None:
      set_ylim = p9.ylim(y_lim)
    else:
      set_ylim = p9.ylim([lg_df[y_name].min(),lg_df[y_name].max()])

    df_plot = ( p9.ggplot(lg_df,
      p9.aes( x=x_name ,y=y_name, fill=x_name )) +
      p9.geom_violin(width=.75, draw_quantiles=Quant, show_legend=False) + 
      p9.ggtitle(title) + p9.theme_classic() + set_ylim +
      p9.theme( text = p9.element_text(size=12, color='black'), 
          axis_text_x = p9.element_text(angle=33),
          panel_grid_major_y = p9.element_line(color='gray', alpha=.5) ) ) 

    p9.ggsave(filename='{0}.violin.{1}'.format(outpref, img), plot=df_plot, 
              dpi=dpi, format=img, width=8, height=6, units='in' )

  else:
    ## Seaborn method
    import seaborn as sns
    sns.set(style='whitegrid')

    ax = sns.violinplot(x=x_name, y=y_name, data=lg_df,
                        linewidth=1, inner='box')
    if title: ax.set_title(title)
    if y_lim is not None: ax.set(ylim=y_lim)

    plt.savefig('{0}.violin.{1}'.format(outpref, img), figsize=(8,6),
                  format=img, dpi=dpi)
    plt.clf()


######################################################################
def UserInput():
  p = ArgumentParser(description='Command Line Arguments')

  p.add_argument('-i', dest='infile', required=True, nargs="+",
                  help='Plot for data files (e.g.: x.txt y.txt z.txt)')
  p.add_argument('-o', dest='outpref', required=True,
                  help='Output prefix')

  p.add_argument('-n', dest='col_names', required=False, nargs="+",
                  help='Custom Column names (e.g.: x_dist y_dist z_dist)')
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

  p.add_argument('-p', dest='use_p9', action='store_true',
                  help='Use Plotnine styling (Def: Seaborn)')

  args=p.parse_args()
  return args
######################################################################
if __name__ == '__main__':
  main()
