#!/bin/tcsh

#
#	Peter M.U. Ung @ MSSM
#	
#	v1.0	16.11.?
#	v1.1	16.12.02	wallch, basket, spotify
#	v2.0	16.12.02	separate build-essential and non-essential
#
#	'Essential' and non-essential Ubuntu packages installation
#	Package subjected to change due to package update/depreciated
#

if ($#argv == 0) then
echo '  > x.csh [update|build|noness|python|science|java]'
  exit
endif
# apt-get for ubuntu


if ($argv[1] == 'update') then
  sudo apt-get update
  sudo apt-get upgrade
  exit
endif

if ($argv[1] == 'build') then
  sudo apt-get install \
  build-essential ccache cmake bzip2 zlib1g-dev csh tcsh \
  ubuntu-desktop lxde xauth xorg openbox lightdm plymouth \
  xserver-xorg-core xserver-xorg wget \
  openmpi-bin libopenmpi-dev libxi-dev libxmu-dev \
  nedit vim emacs gnome-control-center \
  gparted cifs-utils apt-file sysstat trash-cli \
  autotools-dev autoconf automake gcc g++ gfortran htop llvm clang \
  openssh-server openssh-client backintime-common backintime-gnome \
  python-pip python3-pip python-dev python-setuptools python-numpy \
  python-reportlab python-pandas python3-tk \
  libfreetype6-dev bioperl python-cairosvg python3-cairosvg \
  sqlite3 libsqlite3-dev libboost-dev libboost-system-dev \
  libboost-thread-dev libboost-serialization-dev libssl-dev \
  swig git pdftk \
  software-properties-common apt-transport-https code
  
  wget https://mirrors.kernel.org/ubuntu/pool/main/libp/libpng/libpng12-0_1.2.54-1ubuntu1_amd64.deb
  dpkg -i libpng12-0_1.2.54-1ubuntu1_amd64.deb
 
  exit
endif

if ($argv[1] == 'noness') then
  sudo apt-get install \
  gedit tasque wallch basket vlc apcupsd apcupsd-cgi gimp
  exit
endif

## Java update quite often, check if jdk-11 or oracle-13 is most updated
if ($argv[1] == 'java') then
  sudo add-apt-repository ppa:linuxuprising/java
  sudo apt-get update
  sudo apt-get upgrade
  sudo apt-get install default-jre default-jdk \
  openjdk-11-jdk \
  oracle-java13-set-default
  java -version
  exit
endif

if ($argv[1] == 'science') then
  sudo add-apt-repository ppa:graphics-drivers/ppa
  sudo apt-get update
  sudo apt-get upgrade

  sudo apt-get install \
  pymol python-scipy python-biopython python-rdkit librdkit1 rdkit-data \
  openbabel apbs \
  r-base r-base-dev libatlas3-base libopenblas-base \
  r-cran-ncdf4 netcdf-bin libnetcdf-dev \
  clustalw clustalo t-coffee mafft dialign-tx-data dialign-tx poa probcons \
  muscle kalign amap-align tm-align proda ncbi-blast+ blast2 mustang \
  prank freeglut3 freeglut3-dev wkhtmltopdf \
  libhdf5-serial-dev
  
  echo ''
  echo '  ## Also download and install from the source: ##'
  echo '  ##   KNIME, RStudio, Microsoft R Open         ##'
  echo '  ##   Visual Studio Code, FireFox, Chrome      ##'
  echo '  ##   Jalview2, ChemAxon, LigPlot+             ##'
  echo ''
  exit
endif

if ($argv[1] == 'cuda') then
  sudo add-apt-repository ppa:graphics-drivers/ppa
  sudo apt-get update
  sudo apt-get upgrade

  sudo apt-get install libcublas-dev 
  echo ' go to Nvidia website to download the current CUDA driver '
endif


if ($argv[1] == 'python') then
  sudo add-apt-repository ppa:bit-team/stable
  sudo apt-get update
  sudo apt-get install \
  python-pip python-keyring python3-keyring python-gnomekeyring \
  python-dev libjbig-dev libjpeg-dev libjpeg8-dev libpng3 libpng-dev \
  libfreetype6-dev zlib1g-dev libtiffxx5 libtiff5-dev tables \
  python-rpy2 python-dbus python3-dbus python-pyqt5

  # will have to run these install/upgrade manually by copy/paste the list
  # 'cairosvg' is python3 only
  set pip_list = "\
virtualenv numpy scipy matplotlib pandas seaborn setuptools testresources\
scikit-learn scikit-image scikit-misc sklearn-pandas ipython jupyter \
openpyxl xlwt XlsxWriter plotnine plotly openbabel griddataformats \
pathos statsmodels weblogo ContactVis \
Pillow tqdm freesasa cairosvg spacy \
cython mdtraj chembl_webresource_client biopython povme pandarallel"

  set conda_regular = "\
numpy scipy matplotlib pandas scikit-learn ipython jupyter openpyxl xlwt \
XlsxWriter pillow boost tqdm cairo cython curl "

  set conda_forge = ['conda-forge pathos rdkit plotnine jpype1 cairosvg',\
  'scikit-image libxml2 lxml dicttoxml xmltodict griddataformats', \
#  'conda-forge spacy beautifulsoup4', \
  'conda-forge freeglut xorg-libx11 tabulate biopython zlib',\
  'conda-forge mdtraj mdanalysis dask-ml dask swifter', \
  'r rpy2 r-xml2', 'psi4 psi4 resp', \
  'openbabel openbabel', 'chembl chembl_webresource_client', \
  'mmcauliffe pyqt5 qt5', 'samoturk pymol', 'hydroid freesasa', \
  'salilab modeller' ]

## pip from Ubuntu 18.04 will only go to pip3, use pip2.7 mnually for python2.7
#  sudo pip2.7 install --upgrade pip2.7
#  sudo pip3   install --upgrade pip3
  sudo -H pip2.7 install --user --upgrade $pip_list
  sudo -H pip3   install --user --upgrade $pip_list

  ## > conda create --name cdpy2 python=2
  ## > conda create --name cdpy3 python=3

  foreach item ($conda_forge)
    conda install --name cdpy2 -c $item
    conda install --name cdpy3 -c $item
  end
  conda install --name cdpy2 $conda_regular
  conda install --name cdpy3 $conda_regular


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
# - R studio packages - 
# Matrix dplyr tidyverse reshape2 data.table scales gtable purr plyr
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
# download from https://salilab.org/modeller/download_installation.html
# activate Modeller by using the following cmd and activation key:
#
# > sudo env KEY_MODELLER=MODELIRANJE dpkg -i modeller_xxxxxxxxx.deb
#
#######
