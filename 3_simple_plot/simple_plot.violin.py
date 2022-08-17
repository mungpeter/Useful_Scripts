#!/usr/bin/env python3

##########################################################################
#
#  Peter MU Ung @ MSSM/Yale
#
#  v1	19.12.27
#  v2	21.06.26  update with functions

#  Do very simple violin-type histogram for *multiple* data files at once
#
##########################################################################

import sys
msg = '''\n  > {0}
    -i <+>    [ Data file(s) ] # separated by space; 1 or 2 columns; only use last col
    -o < >    [ Output prefix ]
  Optional:
    -n <+>    [ Custom Colnames matching data file order (e.g.: x_id y_id z_id) ]
    -c < >    [ Column number in file(s) to be read (Def: last column) ]
    -d < >    [ Delimiter       (Def:'\s+') ]
    -x < >    [ Name for x-axis (Def: Item) ]
    -y < >    [ Name for y-axis (Def: Distrib) ]
    -t < >    [ Name for title  (Def: None)  ]
    -w < >    [ Linewidth (Def: 1.0) ]
    -rot < >  [ Rotate x-tick label by degree (Def: 0 | 33 is good) ]
    -l <+>    [ Set [bottom top] y-limits (Def: None) ]
    -p        [ Use Plotnine plotting method (Def: Seaborn) ]
    -hor <+>  [ Add horizontal line(s), y = input (def: None) ]
    -col <+>  [ Vertical/Horizontal line color (def="red") ]
    -img < >  [ Figure format: png|jpg|svg|eps|pdf (Def: png) ]
    -siz <+>  [ Figure x/y dimension in inch (Def: 8 6) ]
    -dpi < >  [ Figure quality (Def: 150) ]\n
e.g.> *.py  -i x.txt y.txt z.txt    -o output\n'''.format(sys.argv[0])
if len(sys.argv) == 1: sys.exit(msg)

import matplotlib
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
matplotlib.use('Agg')   # to get around Xwindows when over 'ssh'

from argparse import ArgumentParser

################################################
def main():

  args = UserInput()

  if args.y_lim:
    y_lim = np.array(args.y_lim, dtype=np.float32)
  else:
    y_lim = None
  if args.size:
    size  = np.array(args.size, dtype=np.float32)
  else:
    size  = args.size

###################################

  df_list = [ pd.read_csv(f, sep=args.sep, skipinitialspace=True) 
                for f in args.infile ]

  ## only take input with 1 or 2 columns; for 2 columns, 1st is always removed
  lg_list = []
  for idx, df in enumerate(df_list):
    xdf = pd.DataFrame(df.iloc[:, int(args.col)-1])

    if args.col_names:
      xdf.columns = [args.col_names[idx]]

    lg_list.append(pd.melt(xdf))

  lg_df = pd.concat(lg_list)
  lg_df.columns = [args.x_name, args.y_name]
  print(lg_df)

  ## plotnine method
  if args.use_p9:
    import plotnine as p9
    Quant = [.25,.5,.75]

    if y_lim is not None:
      set_ylim = p9.ylim(tuple(y_lim))
    else:
      set_ylim = p9.ylim([lg_df[args.y_name].min(),lg_df[args.y_name].max()])

    df_plot = ( p9.ggplot(lg_df,
      p9.aes( x=args.x_name ,y=args.y_name, fill=args.x_name )) +
      p9.geom_violin(width=.75, draw_quantiles=Quant, show_legend=False) + 
      p9.ggtitle(args.title) + p9.theme_classic() + set_ylim +
      p9.scale_x_discrete(limits=args.col_names) +
      p9.theme( text = p9.element_text(size=12, color='black'), 
          axis_text_x = p9.element_text(angle=int(args.rotate)),
          panel_grid_major_y = p9.element_line(color='gray', alpha=.5) ) ) 

    if args.hlines:
      for i, h in enumerate(args.hlines):
        df_plot = (df_plot + p9.geom_hline(yintercept=float(h), 
                       color=args.refcolr[i], size=float(args.linewidth)))

    p9.ggsave(filename='{0}.violin.{1}'.format(args.outpref, args.img), 
              plot=df_plot, dpi=int(args.dpi), format=args.img,
              width=size[0], height=size[1], units='in', verbose=False )

  else:
    ## Seaborn method
    import seaborn as sns
    sns.set(style='whitegrid')

    fig, ax = plt.subplots()
    fig.set_size_inches(tuple(size))

    ax = sns.violinplot(x=args.x_name, y=args.y_name, data=lg_df,
                        linewidth=float(args.linewidth), inner='box')

    ## Add custom horizontal (only) lines
    if args.hlines:
      for i, h in enumerate(args.hlines):
        ax.axhline(y=float(h), color=args.refcolr[i], lw=float(args.linewidth))

    ## Adjust labels, titles, max_y-axis
    ax.tick_params(axis='x', rotation=int(args.rotate))
    if args.title:
      ax.set_title(args.title)
    if y_lim is not None:
      ax.set(ylim=tuple(y_lim))

    plt.savefig('{0}.violin.{1}'.format(args.outpref, args.img), 
                format=args.img, dpi=int(args.dpi))
    plt.clf()


######################################################################
def UserInput():
  p = ArgumentParser(description='Command Line Arguments')

  p.add_argument('-i', dest='infile', required=True, nargs="+",
                  help='Plot for data files (e.g.: x.txt y.txt z.txt)')
  p.add_argument('-o', dest='outpref', required=True,
                  help='Output prefix')

  p.add_argument('-n', dest='col_names', required=False, nargs="+", default=None,
                  help='Custom Column names (e.g.: x_dist y_dist z_dist)')
  p.add_argument('-c', dest='col', required=False, default=0,
                  help='Column in file(s) to be plotted (Def: last column)')
  p.add_argument('-d', dest='sep', required=False, default='\s+',
                  help='delimiter       (Def:"\s+")')
  p.add_argument('-x', dest='x_name', required=False, default='Item',
                  help='Name for x-axis (Def: Item)')
  p.add_argument('-y', dest='y_name', required=False, default='Distrib',
                  help='Name for y-axis (Def: Distrib)')
  p.add_argument('-t', dest='title', required=False, default='',
                  help='Name for title  (Def: None)')
  p.add_argument('-rot', dest='rotate', required=False, default=0,
                  help='Rotate x-tick label by degree (Def: 0 | 33 is good)')
  p.add_argument('-l', dest='y_lim', required=False, nargs="+", default=None,
                  help='Set [bottom top] y-limits (Def: None)')

  p.add_argument('-w', dest='linewidth', required=False, default=1.0,
                  help='Line width (Def: 1.0)')
  p.add_argument('-hor', dest='hlines', required=False, nargs='+', default=[],
                  help='Add horizontal line(s), y = input (Def: None)')
  p.add_argument('-col', dest='refcolr',required=False, default=['r'], nargs='+',
                  help='Vertical/Horizontal line color (def="red")')

  p.add_argument('-img', dest='img', required=False, default='png',
                  help='Figure format: png|jpg|svg|eps|pdf (Def: png)')
  p.add_argument('-siz', dest='size', required=False, nargs='+', default=[8,6],
                  help='Figure x/y dimensions in inch  (Def: 8 6)')
  p.add_argument('-dpi', dest='dpi', required=False, default=150,
                  help='Figure quality  (Def: 150)')

  p.add_argument('-p', dest='use_p9', action='store_true',
                  help='Use Plotnine styling (Def: Seaborn)')

  args=p.parse_args()
  return args
######################################################################
if __name__ == '__main__':
  main()
