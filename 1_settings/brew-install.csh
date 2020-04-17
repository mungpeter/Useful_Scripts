#!/bin/bash

#
#	Peter M.U. Ung @ Gene
#	
#	v1.0	20.04.15
#
#

if ($#argv == 0) then
echo '  > x.csh [update|build|noness|python|science|java]'
  exit
endif
# apt-get for ubuntu


if ($argv[1] == 'update') then
  brew update
  brew upgrade
  exit
endif

if ($argv[1] == 'build') then
  brew install \
    cask bzip2 zlib python \
    ccache cmake autoconf automake gcc llvm swig \
    openssh wget vim nedit git poppler htop trash-cli

  brew cask install \
    wkhtmltopdf adobe-acrobat-reader adobe-acrobat-pro

  exit
endif


if ($argv[1] == 'science') then
  brew tap salilab/salilab
  brew tap brewsci/bio

  brew install \
    open-babel blast netcdf modeller \
    muscle clustal-omega kalign prank

#######
#
# - Modeller -
  echo 'activate Modeller by using the following cmd and activation key:'
  echo '> sudo env KEY_MODELLER=MODELIRANJE dpkg -i modeller_xxxxxxxxx.deb'
#
#######

  r-base r-base-dev libatlas3-base libopenblas-base \
  t-coffee mafft dialign-tx-data dialign-tx poa probcons \
  amap-align tm-align proda mustang 

  echo ''
  echo '  ## Also download and install from the source: ##'
  echo '  ##   KNIME, RStudio, Microsoft R Open         ##'
  echo '  ##   Visual Studio Code, FireFox, Chrome      ##'
  echo '  ##   Jalview2, ChemAxon, LigPlot+             ##'
  echo ''
  exit
endif



if ($argv[1] == 'python') then
## For getting Miniconda setup for the first time after installation:
## > conda create --name cdpy7 python=3.7

  # will have to run these install/upgrade manually by copy/paste the list
  # 'cairosvg' is python3 only
  set pip_list = "\
virtualenv numpy scipy matplotlib pandas seaborn setuptools testresources\
scikit-learn scikit-misc sklearn-pandas ipython jupyter \
openpyxl xlwt XlsxWriter plotnine plotly openbabel \
pathos statsmodels weblogo ContactVis \
Pillow tqdm freesasa cairosvg  \
cython mdtraj biopython"

# python 3.6-only chembl_webresource_client

  set conda_regular = "\
numpy scipy matplotlib seaborn pandas ipython jupyter openpyxl xlwt \
XlsxWriter pillow boost tqdm cairo cython curl "

  set conda_forge = ['conda-forge pathos rdkit plotnine jpype1 cairosvg',\
  'conda-forge libxml2 lxml dicttoxml xmltodict', \
  'conda-forge xorg-libx11 tabulate biopython zlib',\
  'conda-forge mdtraj mdanalysis',
  'anaconda scikit-learn'] #
  #'r rpy2 r-xml2', 'psi4 psi4 resp', \
  #'openbabel openbabel', 'chembl chembl_webresource_client', \
  #'mmcauliffe pyqt5 qt5', 'samoturk pymol', 'hydroid freesasa', \
  #'salilab modeller' ]

## pip from Ubuntu 18.04 will only go to pip3, use pip2.7 mnually for python2.7
#  sudo pip3   install --upgrade pip3
  sudo -H pip3   install --user --upgrade $pip_list

  ## > conda create --name cdpy3 python=3
  conda install -n cdpy7 $conda_regular

  foreach item ($conda_forge)
    conda install -n cdpy7 -c $item
  end


  # search for "python pip html module" for HTML module
  exit
endif

## Spotify is now available in Software Manager as .deb package
#if ($argv[1] == 'spotify') then
#  sudo sh -c 'echo "deb http://repository.spotify.com stable non-free" >> /etc/apt/sources.list.d/spotify.list'
#  sudo apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 94558F59
#  sudo apt-get update
#  sudo apt-get install spotify-client
#  exit
#endif



#######
#
## Microsoft R Open is not available on MacOS 10.14 and on, use regular R
## clang (llvm) and gfortran (gcc) should be installed via Homebrew
#
# - R studio packages - 
# install.packages("...")
# Matrix dplyr tidyverse reshape2 data.table scales gtable
# mimi manipulate labeling colorspace RColorBrewer gtools lattice httr
# digest bindr assertthat stringr readxl 
# Plotly ggplot2 gplots ggseqlogo shiny seqinr cowplot
# openssl reticulate RCurl rlang Rcpp pkgconfig modelR ape
# monkeylearn
#
# install.packages(c(arepr IRdisplay evaluate crayon pbdZMQ devtools uuid)) \
# devtools::install_github('IRkernel/IRkernel')  # for R in jupyter
# devtools::install_github('bbc/bbplot')	# BBC plotting style
# 
# install.packages("bio3d", dependencies=TRUE)	# NMA analysis
# ncdf4
#
# special: bioconductor chemineR
#
#######
#
# - Modeller -
# activate Modeller by using the following cmd and activation key:
# > sudo env KEY_MODELLER=MODELIRANJE dpkg -i modeller_xxxxxxxxx.deb
#
#######
