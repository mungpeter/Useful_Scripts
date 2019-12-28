#!/usr/bin/env python3

##########################################################################
#
#  Peter MU Ung @ MSSM/Yale
#
#  v1.   19.12.27
#
#  Do very simple violin-type histogram for *multiple* data files
#
##########################################################################

import sys
msg = '''\n  > {0}
\t[ data files ] # separated by space; 1 or 2 columns; only use last col
\t-o=<>  [ output prefix ]
\tOptional:
\t-d=< > [ delimiter (Def:'\s+') ]
\t-n=<,> [ column name (Def: from header) ] # separated by ','
\t-x=< > [ Name for x-axis ]
\t-y=< > [ Name for y-axis ]
\t-t=< > [ Name for title  ]
\t-p     [ use Plotnine plotting method (Def: Seaborn) ]\n
e.g.> *.py  x.txt y.txt z.txt -o=output\n'''.format(sys.argv[0])
if len(sys.argv) < 2: sys.exit(msg)

import re,glob
import numpy as np
import pandas as pd
import seaborn as sns
sns.set(style='whitegrid')
#sns.set(color_codes=True)
import matplotlib
matplotlib.use('Agg')   # to get around Xwindows when over 'ssh'

import matplotlib.pyplot as plt
import plotnine as p9

################################################
def main():

  print('')
  for idx, var in enumerate(sys.argv):
    if re.search('-d=', var):
      delimiter = var.split('=')[1]
      sys.argv.remove(var)
      print('-d', sys.argv)
    else:
      delimiter = '\s+'

  for idx, var in enumerate(sys.argv):
    if re.search('-n=', var):
      col_names = var.split('=')[1].split(',')
      sys.argv.remove(var)
      print('-n=', col_names)
    else:
      col_names = False

  for idx, var in enumerate(sys.argv):
    if re.search('-o=', var):
      outpref = var.split('=')[1]
      sys.argv.remove(var)
      print('-o=', outpref)

  for idx, var in enumerate(sys.argv):
    if re.search('-x=', var):
      x_name = var.split('=')[1]
      sys.argv.remove(var)
      print('-x=', x_name)
    else:
      x_name = 'variable'

  for idx, var in enumerate(sys.argv):
    if re.search('-y=', var):
      y_name = var.split('=')[1]
      sys.argv.remove(var)
      print('-y=', y_name)
    else:
      y_name = 'value'

  for idx, var in enumerate(sys.argv):
    if re.search('-t=', var):
      title = var.split('=')[1]
      sys.argv.remove(var)
      print('-t=', title)
    else:
      title = ''

  for idx, var in enumerate(sys.argv):
    if re.search('-p', var):
      use_p9 = True
      sys.argv.remove(var)
    else:
      use_p9 = False

  df_list = [pd.read_csv(f, delimiter=delimiter, skipinitialspace=True) 
               for f in sys.argv[1:]]

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
    Quant = [.25,.5,.75]
    df_plot = ( p9.ggplot(lg_df,
      p9.aes( x=x_name ,y=y_name, fill=x_name )) +
      p9.geom_violin(width=.75, draw_quantiles=Quant, show_legend=False) + 
      p9.ggtitle(title) + p9.theme_classic() + 
      p9.theme( text = p9.element_text(size=12, color='black'), 
          axis_text_x = p9.element_text(angle=33),
          panel_grid_major_y = p9.element_line(color='gray', alpha=.5) ) ) 

    p9.ggsave(filename=outpref+'.violin.png', plot=df_plot, dpi=150, 
              width=8, height=6, units='in' )
  else:
    ## Seaborn method
    ax = sns.violinplot(x=x_name, y=y_name, data=lg_df,
                        linewidth=1, inner='box')
    if title: ax.set_title(title)

    plt.savefig(outpref+'.violin.png', dpi=150, figsize=(8,6))



######################################################################
if __name__ == '__main__':
  main()
