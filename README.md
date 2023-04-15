# Useful Scripts for Linux and Python
**General Linux/Python scripts for various purposes**

```
  author: Peter M.U. Ung @ MSSM/Yale/gRED
  vers:   1.
```

- This folder has several folders, each with miscellaneous scripts and setups for different tasks.
```
----- /1_settings         # setups for linux environments
  |-- /2_simple_scripts   # scripts for common linux utility
  |-- /3_simple_plot      # scripts for very simple plotting
```
  

#######################################################################################
- **Initializing a new Linux (Ubuntu) with common packages**
```
> apt-get.csh
    [update|build|noness|python|science|java]
       
     update:  update/upgrade currently installed packages
     build:   install essential "build" linux packages
     noness:  install non-essential linux packages
     science: install "science"-related linux packages
     python:  install often-used python pacakges, including Conda packages
     java:    install Java OpenJDK and Oracle
     Other:   inside this script, there are list of RStudio and Conda packages
```
- A quick way to install essential and common Linux packages, and for Python. Also serve as a library of what have been and should be installed.

#######################################################################################
- **Personalized linux .tcshrc/.cshrc and .vimrc scripts, etc.**
```
> cshrc    # for csh and tcsh
> vimrc
> pymolrc
```
- Add "." to convert them to system scripts .cshrc and .vimrc

#######################################################################################
- **Python manager: Miniconda settings**
- Save an existing conda environment to a .yml file:

```
> conda activate <environment name>
> conda env export | grep -v "^prefix: " > <saved environment>.yml
```

- Create a new environment using a .yml file:
```
> conda env create --name <new environment> --file=<saved environment>.yml
```

#######################################################################################
# Create link between GitHub server and Visual Studio Code
**Link to GitHub**
- First, register the computer in Github. In GitHub website, under **User** --> **Settings** --> **SSH and GPG keys**, add the ssh key via **New SSH key**. Will need to do this for every computer to link to GitHub.
- Getting the RSA SSH key from the computer (MacOS/Linux) terminal by using **ssh_keygen**. When prompt, enter **nothing** to the questions. This will generate a key stored in the file **id_rsa** in **~/.ssh**. Copy the SSH key to GitHub. Once done, GitHub will recognize the computer.
```
> ssh-keygen

Generating public/private rsa key pair.
Enter file in which to save the key (/home/ylo/.ssh/id_rsa): 
Enter passphrase (empty for no passphrase): 
Enter same passphrase again: 
Your identification has been saved in /home/ylo/.ssh/id_rsa.
Your public key has been saved in /home/ylo/.ssh/id_rsa.pub.
The key fingerprint is:
SHA256:Up6KjbnEV4Hgfo75YM393QdQsK3Z0aTNBz0DoirrW+c ylo@klar
The key's randomart image is:
+---[RSA 2048]----+
|    .      ..oo..|
|   . . .  . .o.X.|
|    . . o.  ..+ B|
|   .   o.o  .+ ..|
|    ..o.S   o..  |
|   . %o=      .  |
|    @.B...     . |
|   o.=. o. . .  .|
|    .oo  E. . .. |
+----[SHA256]-----+

> cat ~/.ssh/id_rsa.pub
ssh-rsa FOW9TUQ2J09Jqp4t0u009UGQ0409QJA.... <username>@<localhost>
```


> ---
**Upload files to GitHub**

- In GitHub website, create a new repository.
- In the empty repository, in the green "Clone or download", copy the SSH key in "Use SSH"
- In the shell terminal, go to the folder that will be linked to the Github.

```
> cd repository_folder/
> git init
> git remote add origin <SSH key of the GitHub repository>
> git pull origin master
> code .
```
- Once VSCode is open from inside the directory with the soon-to-be-uploaded codes, via the **Source Control** tab (Ctrl+Shift+G), **Stage Change (+)** to single or all files, then **Commit** (Check mark), then in the _lower left corner_ click the _"cloud-looking thing"_ to upload changes made to the files to GitHub. After the first submit, the _"cloud-looking thing"_ will change into a _"cycle-looking thing"_.

#######################################################################################
- **Simple scripts**

```
-- /2_simple_scripts
           |---- combine_column.py
           |---- extract_column.py
           |---- sum-col.py
           |
```

- very simple utility scripts, like extracting columns from a file; adding columns together, etc.

#######################################################################################
- **Simple plotting**

```
-- /3_simple_plot
        |---- simple_plot.heatmap.py
        |---- simple_plot.histo.py
        |---- simple_plot.line.py
        |---- simple_plot.scatter.py
        |---- simple_plot.violin.py
        |-------- examples
                     |---- example_heatmap.sh
                     |---- pi_h646.violin.png
                     |---- pi_y207w-h646.histo.png
```

- for very simple plotting of data file(s). Plot of a single line of data over time; histrogram (distribution) of a data file; or histogram of several data files as violin plot.

#######################
- **Heatmap plot**
```
> ./simple_plot.heatmap.py
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
e.g.> *.py -in x.txt y.txt -cols 2 2 -out out.svg -xlim 0 5 -ylim 0 5 -smooth 1.5
```

#######################
- **Single-Line plot**
```
> ./simple_plot.line.py
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
    -col < >   [ Vertical/Horizontal line color (def="red") ]
    -rot < >   [ Rotate x-tick label by degree (Def: 0 | 33 is good) ]
    -img < >   [ Figure format: png|jpg|svg|eps|pdf (Def: png) ]
    -siz <+>   [ Figure x/y dimension in inch (Def: 8 6) ]
    -dpi < >   [ Figure quality (Def: 150) ]\n
e.g.> *.py  -a '.txt'
  or
    > *.py  -i data.txt -s -m
```
![line](https://github.com/mungpeter/Useful_Scripts/blob/master/3_simple_plot/examples/pi_y207w-h646.png)

######################
- **Histogram of single data**
```
> ./simple_plot.histo.py
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
    > *.py  -f data.txt -s
```
![histo](https://github.com/mungpeter/Useful_Scripts/blob/master/3_simple_plot/examples/pi_y207w-h646.histo.png)

#####################
- ** 2D-Scatter plot **
```
> ./simple_plot.scatter.py
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
    > *.py  -f data.txt -s
```
![histo](https://github.com/mungpeter/Useful_Scripts/blob/master/3_simple_plot/examples/fgf21-s1-wt.dpeaks.dvd_plot.txt.scatter.png)

##################
- **Violin plot (multi-histrogram)**
```
> ./simple_plot.violin.py
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
    -col < >  [ Vertical/Horizontal line color (def="red") ]
    -img < >  [ Figure format: png|jpg|svg|eps|pdf (Def: png) ]
    -siz <+>  [ Figure x/y dimension in inch (Def: 8 6) ]
    -dpi < >  [ Figure quality (Def: 150) ]

e.g.> *.py pi_h646.1.txt.bz2   
        -i pi_h646.1.txt.bz2 pi_h646.1.txt.bz2 pi_h646.1.txt.bz2
        -o pi_h646 
        -n pi_a208w-h646 pi_r203w-h646 pi_y207w-h646 
        -x pi_interact -y 'distance (Å)'
```
![violin](https://github.com/mungpeter/Useful_Scripts/blob/master/3_simple_plot/examples/pi_h646.violin.png)

#######################################################################################
- **Required packages:**
```
csh/tcsh      # shell

python        # 3.7.2+
  numpy       # 1.17.4
  pandas      # 0.24.1+
  matplotlib  # 3.0.2+
  seaborn     # 0.9.0
  plotnine    # 0.5.1
  argparse    # 1.1
  pathos      # 0.2.3
```
