#!/usr/bin/env python3

##########################################################################
#
#  Peter MU Ung @ gRED
#
#  v1   21.07.08
#
#  Do very generalized 2D-histogram with frequency shown as heatmap
#  Input files will have matching number of rows, and the rows of the 2
#  files are corresponding to one another
#  Max/Min of X/Y-axis are auto-detected and bin size is adjust to yield
#  same number of bins on both axes.
#
##########################################################################

import sys
msg = '''\n  > {0}
    -in   <+> [ Input:  if 1 file, minimum 2 columns; if 2 files, minimum 1 column ]
    -cols <+> [ Column: if 1 file, specify 2 columns; if 2 files, 1 column ]
    -out  < > [ Output figure name with extension; format: png|jpg|svg|eps|pdf ]\n
  Optional:
    -nohead   [ Flag if No header in data file(s) ]
    -comm < > [ Input comment to ignore rest of the line (Def: None) ]
    -sep  < > [ Delimiter (Def:'\s+') ]\n
    -bin    < >  [ Number of bin on X/Y-axes (Def: 20) ]
    -fract  < >  [ Fraction of the maximum Histogram value to display (Def: 0.95) ]
    -smooth < >  [ Histogram data smoothening coefficient (Def: 1.15) ]
    -t_step < >  [ Colorbar tick spacing per histogram digits unit (Def: 4) ]
    -c_step < >  [ Histo Contour spacing per histogram digits unit (Def: 4) ]\n
    -xlim <+> [ X-axis lower and upper limits (Def: None) ]
    -ylim <+> [ Y-axis lower and upper limits (Def: None) ]
    -w    < > [ Line width (Def: 1.0) ]
    -ver  <+> [ Add vertical line(s), x = input (def: None) ]
    -hor  <+> [ Add horizontal line(s), y = input (def: None) ]
    -col  < > [ Vertical/Horizontal line color (def="red") ]
    -tick < > [ Number of ticks on X/Y-axes, auto=6 (Def: auto) ] * need xlim/ylim
    -xlab < > [ Name for X-axis (Def: Item_1) ]
    -ylab < > [ Name for Y-axis (Def: Item_2) ]
    -t < >    [ Figure title  (Def: None) ]
    -dim <+>  [ Figure x/y dimension in inch (Def: 7.0 5.5) ]
    -dpi < >  [ Figure quality (Def: 150) ]\n
e.g.> *.py -in x.txt y.txt -cols 2 2 -out out.svg -xlim 0 5 -ylim 0 5 -smooth 1.5\n'''.format(sys.argv[0])
if len(sys.argv) < 4: sys.exit(msg)

import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt

from scipy import ndimage
from argparse import ArgumentParser

font = {'family': 'Arial'}
mpl.rc('font', **font)
mpl.use('Agg')   # to get around Xwindows when over 'ssh'

######################################################################
def main():

  args = UserInput()
  cols   = np.array(list(map(int, args.cols)))-1  ## data columns to extract
  xlim   = list(map(float, args.xlim)) if args.xlim else False
  ylim   = list(map(float, args.ylim)) if args.ylim else False
  size   = list(map(float, args.size))

  ## collect and clean up input data
  data = CollectData(args.infile, args.sep, args.noheader, args.comment, cols)

  # convert 2D data into histogram and generate figure settings
  fig_obj = FigureData( data, args.bins, args.fraction, args.smooth, args.t_step, args.c_step )

  # generate figure
  GenerateImage( fig_obj, xlim, ylim, args.ticks, args.xlabel, args.ylabel, args.img_name,
                 size, args.dpi, args.linewidth, args.vlines, args.hlines, args.refcolr )


############################################################################
## Collect data in X-axis and Y-axis as list of lists; can be single file with
## 2 data columns, or 2 files with single data column
def CollectData( infile, sep, noheader, comment, cols ):

  ## If input is 2 files with single data column
  if len(infile) > 1:
    xy = []
    for i, f in enumerate(infile):
      if not noheader:
        xy.append(pd.read_csv(f, sep=sep, comment=comment, skipinitialspace=True).iloc[:,cols[i]].to_numpy())
      else:
        xy.append(pd.read_csv(f, sep=sep, header=None, comment=comment, skipinitialspace=True).iloc[:,cols[i]].to_numpy())
  else:  ## if input is 1 file with 2 data columns
    if not noheader:
      df = pd.read_csv(infile[0], sep=sep, comment=comment, skipinitialspace=True).iloc[:,cols].to_numpy()
    else:
      df = pd.read_csv(infile[0], sep=sep, header=None, comment=comment, skipinitialspace=True).iloc[:,cols].to_numpy()
    xy = np.asarray(list(zip(*df)))

  return xy


############################################################################
## extract input residue dihedral angles and generate figure settings
def FigureData( data, bins, fraction, smooth, t_step, c_step ):

  # Generate normalized 2D histogram (array of array)
  Histo, x_bins, y_bins = np.histogram2d(data[0], data[1], 
                                bins=(int(bins)+1,int(bins)+1), density=True)

  xbin_step = abs(x_bins[0] - x_bins[1])
  ybin_step = abs(y_bins[0] - y_bins[1])

  # Smoothening the 2D histogram data
  Sigma = [ (max(x_bins)-min(x_bins)) * float(smooth)/len(x_bins),
            (max(y_bins)-min(y_bins)) * float(smooth)/len(y_bins) ]
  smooth_hist = ndimage.filters.gaussian_filter(Histo, sigma=Sigma)

  # get scientific notation, then set the cutoff to a fraction of maximum
  max_nm = float(np.max(smooth_hist))
  digits = np.ceil(float(('{:e}'.format(max_nm)).split('e')[0]))
  powers = int('{:e}'.format(max_nm).split('e')[1])
  h_max  = np.float('{0}e{1}'.format(digits, powers))

  # numeric format: if powers <= 0, use normal; if > 0, use scientific notion
  if powers < -1:
    num_format = '%.1e'
  else:
    num_format = '%.2f'

  # introduce a cutoff to histogram data
  histo2d = smooth_hist - (h_max*(1-float(fraction)))

  # side bar tick, maximum = histogram value
  cbar_ticks = np.linspace( 0, h_max, num=int(digits*float(t_step))+1 )

  # Contour levels, set to be 'c_step' of the histo value, default is 4x
  levels = np.linspace( 0, h_max, num=int(digits*float(c_step))+1 )

  # X- and Y-axes min and max, will be stretch to be equal
  extent = [  x_bins[0] - xbin_step, x_bins[-1]+ xbin_step,
              y_bins[-1]+ ybin_step, y_bins[0] - ybin_step  ]

  # data is transpose to get correct orientation
  # im_extent and im_colors are dummy value to generate holder blank plot
  fig_obj = ImageData( histo2d=histo2d )
  fig_obj.levels = levels
  fig_obj.extent = extent
  fig_obj.bins   = int(bins)
  fig_obj.format = num_format
  fig_obj.im_extent = extent
  fig_obj.im_colors = mpl.colors.ListedColormap(['#FFFFFF'])
  fig_obj.cbar_ticks = cbar_ticks
  
  return fig_obj


############################################################################
## Generate Ramachandran heat map
def GenerateImage( fig_obj, xlim, ylim, ticks, xlabel, ylabel, img_name, 
                   figsize, dpi, linewidth, vlines, hlines, refcolr ):

  plt.figure(2, figsize=figsize)
  colors = mpl.cm.jet

  bar_extend  = 'neither'
  plot_extend = 'neither'

  ## imshow forces figure to have axis ratio 1:1
  ## issue with y-axis data ordering, deal with it by inversing y-axis
  ## generate a fake imshow with dummy matrix to get axis ratio 1:1
#  plt.imshow( np.zeros(shape=(fig_obj.bins, fig_obj.bins)),
#    extent=fig_obj.im_extent, cmap=fig_obj.im_colors)

  ## overlay input AA histogram heat map on top of reference map, if exists
  plt.contourf( fig_obj.histo2d.transpose(), 
                origin='upper', extend=plot_extend, alpha=0.6,
                extent=fig_obj.extent, levels=fig_obj.levels,
                cmap=mpl.cm.get_cmap(colors, len(fig_obj.levels)) )

  ## create colorbar instance on side based on last data input
  cbar = plt.colorbar(ticks=fig_obj.cbar_ticks, format=fig_obj.format, aspect=20 )
  bar_label = '% Population'
  cbar.ax.set_ylabel(bar_label, rotation=270, fontsize=18, labelpad=20)
  cbar.ax.tick_params(labelsize=14)

  ## then overlay contour lines on top of heat map
  plt.contour( fig_obj.histo2d.transpose(), 
              extent=fig_obj.extent, levels=fig_obj.levels,
              origin='upper', colors='black', linewidths=0.67, alpha=0.4 )

  ## Add custom vertical/horizontal lines
  if vlines:
    for v in list(map(float,vlines)):
      plt.axvline(x=v, color=refcolr, lw=float(linewidth))
  if hlines:
    for h in list(map(float,hlines)):
      plt.axhline(y=h, color=refcolr, lw=float(linewidth))

  ## Adjust labels, titles, max_y-axis
  plt.xticks(fontsize=14)
  plt.yticks(fontsize=14)
  if xlim:
    plt.xlim(xlim)
    if ticks: plt.xticks(np.linspace(xlim[0], xlim[1], num=int(ticks)), fontsize=14)
  if ylim:
    plt.ylim(ylim)
    if ticks: plt.yticks(np.linspace(ylim[0], ylim[1], num=int(ticks)), fontsize=14)

  plt.xlabel(xlabel, fontsize=14)
  plt.ylabel(ylabel, fontsize=14)
  plt.grid(True, linestyle='--', alpha=0.75)

  plt.savefig(img_name, bbox_inches=0, dpi=int(dpi))


############################################################################
## Create an image object that can flexibly hold other kwargs input
class ImageData(object):
  def __init__( self, histo2d='', **kwargs):
    self.histo2d = histo2d



######################################################################
def UserInput():
  p = ArgumentParser(description='Command Line Arguments')

  p.add_argument('-in', dest='infile', required=True, nargs="+",
                  help='Input: if 1 file, specify 2 columns; if 2 files, 1 column')
  p.add_argument('-cols', dest='cols', required=True, nargs='+',
                  help='Column in file(s): if 1 file, specify 2 columns; if 2 files, 1 column')
  p.add_argument('-out', dest='img_name', required=True,
                  help='Output figure name with extension; format: png|jpg|svg|eps|pdf')

  p.add_argument('-noheader', dest='noheader', required=False, action='store_true',
                  help='No header in data file(s)')
  p.add_argument('-comm', dest='comment', required=False, default=None,
                  help='Input comment to ignore rest of the line (Def: None)')
  p.add_argument('-sep', dest='sep', required=False, default='\s+',
                  help='delimiter (Def:"\s+")')

  p.add_argument('-dim', dest='size', required=False, nargs='+', default=[7,5.5],
                  help='Figure x/y dimensions in inch  (Def: 7 5.5)')
  p.add_argument('-dpi', dest='dpi', required=False, default=150,
                  help='Figure quality  (Def: 150)')

  p.add_argument('-bin', dest='bins', required=False, default=20,
                  help='Number of bins for X/Y-axes (Def: 20)')
  p.add_argument('-smooth', dest='smooth', required=False, default=1.15,
                  help='Histogram data smoothening coefficient (def: 1.15)')
  p.add_argument('-fract', dest='fraction', required=False, default=0.95,
                  help='Fraction of the maximum Histogram value to display (Def: 0.95)')
  p.add_argument('-t_step', dest='t_step', required=False, default=4,
                  help='Colorbar tick spacing per Histogram digits value (def: 4)')
  p.add_argument('-c_step', dest='c_step', required=False, default=4,
                  help='Histogram Contour spacing per Histogram digits value (def: 4)')

  p.add_argument('-w', dest='linewidth', required=False, default=1.0,
                  help='Line width (Def: 1.0)')
  p.add_argument('-ver', dest='vlines', required=False, nargs='+', default=[],
                  help='Add vertical line(s), x = input (Def: None)')
  p.add_argument('-hor', dest='hlines', required=False, nargs='+', default=[],
                  help='Add horizontal line(s), y = input (Def: None)')
  p.add_argument('-col', dest='refcolr',required=False, default='red',
                  help='Vertical/Horizontal line color (def="red")')

  p.add_argument('-xlim', dest='xlim', required=False, nargs="+", default=False,
                  help='X-axis lower and upper limits (Def: None)')
  p.add_argument('-ylim', dest='ylim', required=False, nargs="+", default=False,
                  help='Y-axis lower and upper limits (Def: None)')
  p.add_argument('-tick', dest='ticks', required=False, default=False,
                  help='Number of ticks on X/Y-axes, auto=6 (Def: auto) * need xlim/ylim')
  p.add_argument('-xlab', dest='xlabel', required=False, default='Item_1',
                  help='Name for X-axis (Def: Item_1)')
  p.add_argument('-ylab', dest='ylabel', required=False, default='Item_2',
                  help='Name for Y-axis (Def: Item_2)')
  p.add_argument('-t', dest='title', required=False, default='',
                  help='Figure Title  (Def: None)')

  args=p.parse_args()
  return args


######################################################################
if __name__ == '__main__':
  main()
